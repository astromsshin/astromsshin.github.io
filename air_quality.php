<?php
$str1 = date('Y-m-d', time() - (24*60*60));
$str2 = date('Y-m-d', time());
$str3 = date('H', time() - (60*60));
$str4 = date('H', time());
header('Location: http://www.airkorea.or.kr/realSearch_pop?stationCode=525141&period=undefined&dateDiv=1&from_date='.$str1.'&to_date='.$str2.'&from_date_hour='.$str3.'&to_date_hour='.$str4);
?>
