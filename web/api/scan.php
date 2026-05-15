<?php
header("Content-Type: application/json");
require_once __DIR__."/../lib/db.php";
require_once __DIR__."/../lib/sanitize.php";
require_once __DIR__."/../lib/analyzer_client.php";

$body = json_decode(file_get_contents("php://input"), true);
$raw  = $body["url"] ?? $_POST["url"] ?? $_GET["url"] ?? "";
$url  = clean_url($raw);

if(!$url){
	http_response_code(400);
	echo json_encode(["error" => "Invalid URL"]);
	exit;
}

$result = analyzer_scan($url);

// Upsert urls row
$stmt = $con->prepare("SELECT url_id, scan_count FROM urls WHERE url = :u");
$stmt->execute([":u" => $url]);
$existing = $stmt->fetch();

if($existing){
	$url_id = $existing["url_id"];
	$con->prepare("UPDATE urls SET last_scanned_at = datetime('now'), scan_count = scan_count + 1 WHERE url_id = :id")
		->execute([":id" => $url_id]);
}else{
	$con->prepare("INSERT INTO urls (url, hostname, scan_count) VALUES (:u, :h, 1)")
		->execute([":u" => $url, ":h" => host_of($url)]);
	$url_id = (int)$con->lastInsertId();
}

$status		= $result["status"] ?? "error";
$score		= $result["score"] ?? null;
$grade		= $result["grade"] ?? null;
$final		= $result["final_url"] ?? null;
$code		= $result["status_code"] ?? null;
$headers	= json_encode($result["headers"] ?? null);
$chain		= json_encode($result["redirect_chain"] ?? null);
$err		= $result["error_message"] ?? null;

$ins = $con->prepare("
	INSERT INTO scans
		(url_id, status, score, grade, final_url, status_code, raw_headers_json, redirect_chain_json, error_message)
	VALUES
		(:url_id, :status, :score, :grade, :final, :code, :headers, :chain, :err)
");
$ins->execute([
	":url_id"	=> $url_id,
	":status"	=> $status,
	":score"	=> $score,
	":grade"	=> $grade,
	":final"	=> $final,
	":code"		=> $code,
	":headers"	=> $headers,
	":chain"	=> $chain,
	":err"		=> $err,
]);
$scan_id = (int)$con->lastInsertId();

if($status === "success" && !empty($result["tests"])){
	$tIns = $con->prepare("
		INSERT INTO scan_tests (scan_id, header_name, status, header_value, points, message)
		VALUES (:s, :n, :st, :v, :p, :m)
	");
	foreach($result["tests"] as $t){
		$tIns->execute([
			":s"  => $scan_id,
			":n"  => $t["header_name"],
			":st" => $t["status"],
			":v"  => $t["header_value"],
			":p"  => (int)$t["points"],
			":m"  => $t["message"],
		]);
	}
}

echo json_encode([
	"scan_id" => $scan_id,
	"url_id"  => $url_id,
	"result"  => $result,
]);
?>
