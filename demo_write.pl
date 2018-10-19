require "./requests_lib.pl"; my @r = send_cmd("relay 0 write 1"); print  $r[0];
