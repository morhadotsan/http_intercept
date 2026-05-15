<?php
header("Content-Type: application/json");
require_once __DIR__."/../lib/db.php";
require_once __DIR__."/../lib/sanitize.php";

$url = clean_url($_GET["url"] ?? "");

if($url){
	$stmt = $con->prepare("
		SELECT s.scan_id, s.status, s.score, s.grade, s.final_url, s.status_code, s.error_message, s.scanned_at, u.url
		FROM scans s
		JOIN urls u ON u.url_id = s.url_id
		WHERE u.url = :u
		ORDER BY s.scanned_at DESC
		LIMIT 100
	");
	$stmt->execute([":u" => $url]);
	echo json_encode(["url" => $url, "scans" => $stmt->fetchAll()]);
}else{
	$stmt = $con->query("
		SELECT u.url_id, u.url, u.hostname, u.last_scanned_at, u.scan_count,
			(SELECT score FROM scans WHERE url_id = u.url_id ORDER BY scanned_at DESC LIMIT 1) AS latest_score,
			(SELECT grade FROM scans WHERE url_id = u.url_id ORDER BY scanned_at DESC LIMIT 1) AS latest_grade
		FROM urls u
		ORDER BY u.last_scanned_at DESC
		LIMIT 200
	");
	echo json_encode(["urls" => $stmt->fetchAll()]);
}
?>
