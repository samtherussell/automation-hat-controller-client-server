#!/usr/bin/perl

use IO::Socket::UNIX;
 
sub send_cmd {
  my $client = IO::Socket::UNIX->new(
    Type => SOCK_STREAM(),
    Peer => "/tmp/hat_controller_socket",
  );

  $client->write($_[0]);
  my $data = "";
  $client->recv($data, 10);
  my ($key, $val) = split /\s/, $data;
  $client->close();
  return ($key, $val);
}

1;
