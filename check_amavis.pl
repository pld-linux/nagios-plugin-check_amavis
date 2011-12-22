#!/usr/bin/perl

use Getopt::Long;
use MIME::Entity;
use Net::SMTP;

my $server = '';
my $port = 10024;
my $from = '';
my $to = '';
my $debug = 0;

my %STATES = (
	"OK" => 0,
	"WARNING" => 1,
	"CRITICAL" => 2,
	"UNKNOWN" => 3,
	"DEPENDENT" => 4,
);

$result = GetOptions (
	"server|s=s"    =>      \$server,
	"port|p=s"      =>      \$port,
	"from|f=s"      =>      \$from,
	"debug|d"      =>      \$debug,
	"to|t=s"        =>      \$to,
);

if (!$server || !$from) {
	print "Please specify server, from\n";
	exit $STATES{UNKNOWN};
}

if (!$to) {
	$to = $from;
}

my $EICAR = <<'EOF';
X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
EOF

my $top = MIME::Entity->build(
	Type    =>"multipart/mixed",
	From    => $from,
	To      => $to,
	Subject => "EICAR test",
	Data    => "This is a test",
);

$top->attach(
	Data    => $EICAR,
	Type    => "application/x-msdos-program",
	Encoding        => "base64",
);

my $smtp = new Net::SMTP(
	$server,
	Port => $port,
	Debug => $debug,
);

if (!$smtp) {
	print "CRITICAL - amavisd-new server unreachable\n";
	exit $STATES{CRITICAL};
}

$smtp->mail($from);
$smtp->to($to);
$smtp->data();
$smtp->datasend($top->stringify);
$smtp->dataend();
my $result = $smtp->message();
$smtp->close();

if ($result =~/2.7.[01] Ok, discarded/) {
	print "OK - All fine\n"
} else {
	print "CRITICAL - amavisd-new returned $result";
}
