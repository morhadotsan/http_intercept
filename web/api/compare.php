<?php
header("Content-Type: application/json");
require_once __DIR__."/../lib/db.php";
require_once __DIR__."/../lib/sanitize.php";

$a = clean_int($_GET["a"] ?? 0);
$b = clean_int($_GET["b"] ?? 0);

if(!$a || !$b){
	http_response_code(400);
	echo json_encode(["error" => "Provide two scan ids: a and b"]);
	exit;
}

function load_scan($con, $id){
	$stmt = $con->prepare("
		SELECT s.*, u.url
		FROM scans s
		JOIN urls u ON u.url_id = s.url_id
		WHERE s.scan_id = :id
	");
	$stmt->execute([":id" => $id]);
	$scan = $stmt->fetch();
	if(!$scan) return null;

	$tests = $con->prepare("SELECT header_name, status, header_value, points, message FROM scan_tests WHERE scan_id = :id");
	$tests->execute([":id" => $id]);
	$scan["tests"] = $tests->fetchAll();
	return $scan;
}

$sa = load_scan($con, $a);
$sb = load_scan($con, $b);

if(!$sa || !$sb){
	http_response_code(404);
	echo json_encode(["error" => "Scan not found"]);
	exit;
}

// Build per-header diff
$indexA = [];
$indexB = [];
foreach($sa["tests"] as $t) $indexA[$t["header_name"]] = $t;
foreach($sb["tests"] as $t) $indexB[$t["header_name"]] = $t;
$names = array_unique(array_merge(array_keys($indexA), array_keys($indexB)));

$diff = [];
foreach($names as $n){
	$ta = $indexA[$n] ?? null;
	$tb = $indexB[$n] ?? null;
	$changed = !$ta || !$tb
		|| $ta["status"] !== $tb["status"]
		|| $ta["header_value"] !== $tb["header_value"]
		|| $ta["points"] !== $tb["points"];
	$diff[] = ["header_name" => $n, "a" => $ta, "b" => $tb, "changed" => $changed];
}

echo json_encode(["a" => $sa, "b" => $sb, "diff" => $diff]);
?>