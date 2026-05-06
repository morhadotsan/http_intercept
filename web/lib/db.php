<?php
try{
	$con = new PDO("sqlite:".__DIR__."/http_intercept_db.sqlite");
	$con->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	$con->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
	$con->exec("PRAGMA foreign_keys = ON");
	
	// Create Tables Here
	createTables($con);
	//addColumnIfMissing($con, "admin", "account_status", "TEXT NOT NULL DEFAULT '250'");
	//print_r(columnExists($con, "admin", "account_status"));
}catch(PDOException $e){
	error_log("Database Connection failed: ".$e->getMessage());
}

function createTables($con){
	try{
		$con->exec("
			CREATE TABLE IF NOT EXISTS `urls` (
				`url_id`				INTEGER PRIMARY KEY AUTOINCREMENT,
				`url`					TEXT NOT NULL UNIQUE,
				`hostname`				TEXT NOT NULL,
				`first_scanned_at`		TEXT NOT NULL DEFAULT (datetime('now')),
				`last_scanned_at`		TEXT NOT NULL DEFAULT (datetime('now')),
				`scan_count`			INTEGER NOT NULL DEFAULT 0
			)
		");
	}catch(PDOException $e){
		error_log("Table (urls) Creation failed: ".$e->getMessage());
	}
	
	try{
		$con->exec("
			CREATE TABLE IF NOT EXISTS `scans` (
				`scan_id`				INTEGER PRIMARY KEY AUTOINCREMENT,
				`url_id`				INTEGER NOT NULL,
				`status`				TEXT NOT NULL CHECK(`status` IN ('success','error')),
				`score`					INTEGER,
				`grade`					TEXT,
				`final_url`				TEXT,
				`status_code`			INTEGER,
				`raw_headers_json`		TEXT,
				`redirect_chain_json`	TEXT,
				`error_message`			TEXT,
				`scanned_at`			TEXT NOT NULL DEFAULT (datetime('now')),
				FOREIGN KEY (`url_id`) REFERENCES `urls`(`url_id`) ON DELETE CASCADE
			)
		");
	}catch(PDOException $e){
		error_log("Table (scans) Creation failed: ".$e->getMessage());
	}
	
	try{
		$con->exec("
			CREATE TABLE IF NOT EXISTS `scan_tests` (
				`test_id`				INTEGER PRIMARY KEY AUTOINCREMENT,
				`scan_id`				INTEGER NOT NULL,
				`header_name`			TEXT NOT NULL,
				`status`				TEXT NOT NULL CHECK(`status` IN ('Present','Missing','Misconfigured')),
				`header_value`			TEXT,
				`points`				INTEGER NOT NULL DEFAULT 0,
				`message`				TEXT,
				FOREIGN KEY (`scan_id`) REFERENCES `scans`(`scan_id`) ON DELETE CASCADE
			)
		");
	}catch(PDOException $e){
		error_log("Table (scan_tests) Creation failed: ".$e->getMessage());
	}
}

function columnExists($con, $table, $column){
    $stmt = $con->prepare("PRAGMA table_info(`$table`)");
    $stmt->execute();
    foreach($stmt->fetchAll(PDO::FETCH_ASSOC) as $col){
        if(strcasecmp($col["name"], $column) === 0) return true;
    }
    return false;
}

function addColumnIfMissing($con, $table, $column, $definition){
    if(!columnExists($con, $table, $column)){
        $con->exec("ALTER TABLE `$table` ADD COLUMN `$column` $definition");
    }
}
?>