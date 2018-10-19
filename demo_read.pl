require "./requests_lib.pl"; my @r = send_cmd("analog 0 read"); print  $r[1];
