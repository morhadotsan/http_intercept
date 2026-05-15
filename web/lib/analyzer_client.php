<?php
function analyzer_url(){
	$base = getenv("ANALYZER_URL");
	if(!$base) $base = "http://127.0.0.1:5000";
	return rtrim($base, "/");
}

function analyzer_scan($url){
	$endpoint = analyzer_url()."/scan";
	$payload = json_encode(["url" => $url]);

	$ch = curl_init($endpoint);
	curl_setopt_array($ch, [
		CURLOPT_RETURNTRANSFER	=> true,
		CURLOPT_POST			=> true,
		CURLOPT_POSTFIELDS		=> $payload,
		CURLOPT_HTTPHEADER		=> ["Content-Type: application/json"],
		CURLOPT_TIMEOUT			=> 30,
	]);
	$body = curl_exec($ch);
	$err  = curl_error($ch);
	$code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
	curl_close($ch);

	if($body === false){
		return ["status" => "error", "error_message" => "Analyzer unreachable: ".$err];
	}
	$decoded = json_decode($body, true);
	if(!is_array($decoded)){
		return ["status" => "error", "error_message" => "Invalid analyzer response (HTTP $code)"];
	}
	return $decoded;
}
?>