;+
; NAME:
;   run_composite
;
; PURPOSE:
;   Produces a composite spectrum using the list of the SDSS spectra
;
; CALLING SEQUENCE:
;   run_composite, plate_fiber_fn, out_fn, verbose
;
; INPUTS:
;   plate_fiber_fn - the file that has four columns: MJD, plate number, fiber id, and redshift
;   out_fn - the filename of the output composite spectrum
;   verbose - 0: without debugging messages, 1: with debugging messages
;
; OUTPUTS:
;   out_fn - the composite spectrum in ASCII format
;
; COMMENTS:
;   In the code, "CHOICE" and "WARNING" need your attention before you run this routine.
;
; PROCEDURES CALLED:
;   idlspec2d, idlspec1d, idlutils, dust
;
; REVISION HISTORY:
;   Jan-2009  Written by Min-Su Shin, Princeton.
;-
;------------------------------------------------------------------------------

PRO run_composite, plate_fiber_fn, out_fn, verbose

; PART I
; setup data array for the composite spectrum
; and other constants
norm_wave = 5550.0 ; 5550A does not have any strong emission lines.
norm_wave1 = norm_wave - 3.0
norm_wave2 = norm_wave + 3.0
; CHOICE A: the normalization option
norm_mean = 1 ;normalization factor from mean = 1
;norm_mean = 0 ;normalization factor from median = 0
; CHOICE B: how to make a composite spectrum
;composite_method = 1 ; weighted-mean combine
composite_method = 0 ; median combine
log_norm_wave = alog10(norm_wave)
log_norm_wave1 = alog10(norm_wave1)
log_norm_wave2 = alog10(norm_wave2)
; CHOICE C: the wavelength range of the output spectrum
;lam_output_range= [2800.0, 9200.0] ; angstrom default = 2800 to 9200
lam_output_range= [3500.0, 9000.0] ; angstrom
log_lam_output_range = alog10(lam_output_range)
logScale = 1.0e-4 ; SDSS scale
n_output = floor((log_lam_output_range[1] - log_lam_output_range[0])/logScale)
log_lam_output = log_lam_output_range[0] + dindgen((log_lam_output_range[1] $
- log_lam_output_range[0]) / logScale) * logScale
lam_output = 10^(log_lam_output)
output_arr = fltarr(n_elements(log_lam_output)) ; output spectrum
var_arr = fltarr(n_elements(log_lam_output)) ; sum of invvar
count_arr = lonarr(n_elements(log_lam_output)) ; count how many spectra are used
n_pix = n_elements(log_lam_output)
IF (verbose GT 0) THEN BEGIN
	print, "# number of output pixels = ", n_pix
	print, "# wavelength range = ", lam_output[0], lam_output[n_pix-1]
	print, "# wavelength range (log10) = ", log_lam_output[0], log_lam_output[n_pix-1]
ENDIF



; (WARNING) PART II
; Reading MJD, plate number, fiber id, and redshift for the SDSS spectra
; four columns : MJD, plate number, fiber id, and redshift
readcol, plate_fiber_fn, mjd_list, plate_list, fiber_list, z_list, ra_list, dec_list, $
FORMAT='L,I,I,F,F,F', COMMENT='#'
num_plate_list = n_elements(plate_list)
print, "# Reading ", plate_fiber_fn, " with ", num_plate_list, " spectra"


; PART III
; loop for SDSS spectra
n_use = 0
; median combine
IF (composite_method EQ 0) THEN BEGIN
	output_arr_temp = fltarr(n_elements(log_lam_output), num_plate_list) ; temporary output spectrum
ENDIF
FOR i=0L, num_plate_list-1 DO BEGIN
	mjd = mjd_list[i]
	plate_num = plate_list[i]
	fiber_id = fiber_list[i]
	z = z_list[i]
	ra = ra_list[i]
	dec = dec_list[i]
	IF (verbose GT 0) THEN BEGIN
		print, "# plate number = ", plate_num, " -> fiber id = ", fiber_id, $
		" with MJD = ", mjd
	ENDIF
	; (WARNING) step 0
	; read one SDSS spectrum
	flux = 0.0
	readspec, plate_num, fiber_id, mjd=mjd, flux=flux, invvar=invvar, loglam=loglam, $
	wave=wave, andmask=andmask, ormask=ormask, objhdr=objhdr, zans=zans, /silent
	; check whether the spectrum has been loaded or not
	IF (n_elements(flux) GT 1) THEN BEGIN
	n_use = n_use + 1

	IF (verbose GT 0) THEN BEGIN
		print, "#... min. & max. lambda = ", wave[0], wave[n_elements(wave)-1]
		print, "#... min. & max. lambda (rest-frame) = ", wave[0]/(1.0+z), wave[n_elements(wave)-1]/(1.0+z)
		print, "#... min. & max. lambda (rest-frame log10) = ", $
	alog10(wave[0]/(1.0+z)), alog10(wave[n_elements(wave)-1]/(1.0+z))
	ENDIF
	; masking out unphysical pixels
	masking_out_pixels, flux, invvar
	; step 1
	; deredshift and rebin the given spectrum
	redindices_rebin, loglam, flux, invvar, z, $
	log_lam_output[0], log_lam_output[n_pix-1], $
	new_log_lam, new_flux, new_invvar
;	FOR j=0L, n_elements(new_invvar)-1 DO BEGIN
;		print, new_log_lam[j], new_flux[j], new_invvar[j]
;	ENDFOR
	; (WARNING) step 2
	; correcting the Galactic extinction
	; if you don't need this correction, comment the following lines.
	wave = 10.0^(new_log_lam)
	alam = ext_ccm(wave)
	glactc, ra, dec, 2000., gl, gb, 1, /deg
	ebv = dust_getval(gl, gb, ipath='/u/schlegel/dustpub/maps/') 
	extvoebv = 3.1
	ext = ebv*alam*extvoebv
	new_flux = new_flux*10.0^(0.4*ext)
	; step 3
	; find the range of acceptable pixels
	; and the normalization factor
	ind = where(new_invvar GT 0.0)
	ind_begin = ind[0]
	ind_end = ind[n_elements(ind) - 1]
	ind = where((new_log_lam GE log_norm_wave1) and (new_log_lam LE log_norm_wave2))
	IF (verbose GT 0) THEN BEGIN
		print, "#... number of pixels for normalization = ", n_elements(ind)
	ENDIF
	IF (norm_mean GT 0) THEN BEGIN
		norm_factor = TOTAL(new_flux[ind])/float(n_elements(ind))
	ENDIF ELSE BEGIN
		norm_factor = MEDIAN(new_flux[ind])
	ENDELSE
	IF (verbose GT 0) THEN BEGIN
		print, "#... normalization factor = ", norm_factor
	ENDIF
	ind = where(new_invvar[ind_begin:ind_end] LE 0.0)
	IF (verbose GT 0) THEN BEGIN
		print, "#... number of bad pixels = ", n_elements(ind)
	ENDIF
	; step 4
	; normalization and sum up
	new_flux = new_flux / norm_factor
	FOR j=0L, n_pix-1 DO BEGIN
		IF (new_invvar[j] GT 0.0) THEN BEGIN
			IF (composite_method EQ 0) THEN BEGIN
				output_arr_temp[j,count_arr[j]] = new_flux[j]
			ENDIF ELSE BEGIN
				output_arr[j] = output_arr[j] + new_flux[j]*new_invvar[j]
				var_arr[j] = var_arr[j] + new_invvar[j]
			ENDELSE
			count_arr[j] = count_arr[j] + 1
		ENDIF
	ENDFOR

	ENDIF

ENDFOR

ind = WHERE(count_arr LE 0)
IF (verbose GT 0) THEN BEGIN
	print, "# number of blank pixels = ", n_elements(ind)
ENDIF
fmt_spec="(F,1X,F,1X,F,1X,I)"
print, "# the number of used spectra = ", n_use
OPENW, 15, out_fn
IF (composite_method EQ 0) THEN BEGIN
	FOR i=0L, n_pix-1 DO BEGIN
		IF (count_arr[i] GT 0) THEN BEGIN
			output_arr[i] = MEDIAN(output_arr_temp[i,0:count_arr[i]-1])
		ENDIF
		PRINTF, 15, FORMAT=fmt_spec, lam_output[i], output_arr[i], var_arr[i], count_arr[i]
	ENDFOR
ENDIF ELSE BEGIN
	FOR i=0L, n_pix-1 DO BEGIN
		IF (count_arr[i] GT 0) THEN BEGIN
			output_arr[i] = output_arr[i] / var_arr[i]
			PRINTF, 15, FORMAT=fmt_spec, lam_output[i], output_arr[i], SQRT(1.0/var_arr[i]), count_arr[i]
		ENDIF ELSE BEGIN
			PRINTF, 15, FORMAT=fmt_spec, lam_output[i], output_arr[i], var_arr[i], count_arr[i]
		ENDELSE
	ENDFOR
ENDELSE
FREE_LUN, 15

	
;format_fit="(I,1X,I,1X,I,1X,21(E,1X))"
;format_cont="(I,1X,I,1X,3(E,1X))"


END
