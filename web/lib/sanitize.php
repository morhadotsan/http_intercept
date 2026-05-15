<?php
function clean_url($input){
	$url = trim((string)$input);
	if($url === "") return null;
	if(!preg_match('#^https?://#i', $url)) $url = "http://".$url;
	$url = filter_var($url, FILTER_SANITIZE_URL);
	if(!filter_var($url, FILTER_VALIDATE_URL)) return null;
	$host = parse_url($url, PHP_URL_HOST);
	if(!$host) return null;
	return $url;
}

function host_of($url){
	return parse_url($url, PHP_URL_HOST) ?: "";
}

function clean_int($input, $default = 0){
	if($input === null || $input === "") return $default;
	return (int)$input;
}
?>