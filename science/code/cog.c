/* Curve of Growth */
/* by Min-Su Shin */
/* It uses GSL routines. */

#include<stdio.h>
#include<math.h>
#include<gsl/gsl_integration.h>

double integrand(double x, void *params)
{
	double tau_0 = *(double *) params;
	double f;
	f = 1.0 - exp(-1.0*tau_0/exp(1.0*x*x));
	return f;
}


int main(int argc, char **argv)
{
	double const c = 3.0e+10; // speed of light : 3.0*10^10 cm/s 
	double b, f, lambda, N, tau_0, F_tau_0, F_tau_0_err, W;
	int i;
	double N_max, N_min, dN;
	FILE* outfile;

	if(argc != 6) {
		printf("Usage : cog.exe [N_max (cm^-2)] [N_min (cm^-2)] [# of N points (float number)] [b(km/s)] [Ouput filename]\n");
		return 1;
	}
	
	N_max = atof(argv[1]);
	N_min = atof(argv[2]);
	dN = atof(argv[3]);
	b = atof(argv[4]);
	b = b*100000.0; // km/s -> cm/s
	outfile=fopen(argv[5],"w");

// FeII
//	double f_array[4] = {0.114, 0.0313, 0.32, 0.239};
//	double lambda_array[4] = {2344.2140, 2374.4612, 2382.7650, 2600.1729};
	
// SiIV
//	double f_array[2] = {0.528, 0.262};
//	double lambda_array[2] = {1393.7550, 1402.7700};

// FeII & SiIV & CIV & AlIII & MgII & SiII
	double f_array[13] = {0.058, 0.114, 0.0313, 0.32, 0.239, 0.528, 0.262, 0.1908, 0.09522, 0.5390, 0.2680, 0.6123, 0.3054};
	double lambda_array[13] = {1608.4511, 2344.2140, 2374.4612, 2382.7650, 2600.1729, 1393.7550, 1402.7700, 1548.195, 1550.77, 1854.7164, 1862.7895, 2796.3520, 2803.5310};
	
	gsl_integration_workspace *w = gsl_integration_workspace_alloc(50000);
	gsl_function int_F;
	int_F.function = &integrand;
	int_F.params = &tau_0;

// you can change the number of trials : i
	for(i=0; i < 1; i++)
	{

	f = f_array[i];
	lambda = lambda_array[i];
	N = N_min;
	dN = (N_max - N_min)/ dN;
	while(N < N_max) 
	{
		tau_0 = (1.497e-10 * f * lambda * N) / b;
		
		gsl_integration_qagiu(&int_F, 0.0, 0.000001, 0.00001, 50000, w, &F_tau_0, &F_tau_0_err);
	
		N = N + dN;
	
		W = lambda*2.0*F_tau_0*b/c;
	
		// the unit of Nf\lambda = cm^-1	
		fprintf(outfile,"%e %e\n", N*f*lambda*1.0e-8, W/lambda);
	}
	
	}

	fclose(outfile);

	return 0;
}
