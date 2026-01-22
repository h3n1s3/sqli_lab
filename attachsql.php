<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
$db_file = "database.db";
try{
    $db = new SQLite3($db_file);
    $db->exec("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)");
    $count = $db->querySingle("SELECT COUNT(*) FROM users");
    if ($count < 100){
        $db->exec('BEGIN');
        $db->exec("INSERT OR IGNORE INTO users (id, username) VALUES (1, 'admin')");
        for ($i =2; $i <= 150; $i++){
            $u = "user_" . $i;
            $db->exec("INSERT OR IGNORE INTO users (id, username) VALUES ($i, '$u')");

        }
        $db->exec('COMMIT');
    }

    $id = isset($_GET['id']) ? $_GET['id'] : '';

} catch (Exception $e) {
    die("Lỗi kết nối DB: " . $e->getMessage());
}
?>
<!DOCTYPE html>
<html>
<body>
    <h1>SQLite Injection Demo (PHP Environment)</h1>
    <p>Hãy thử inject vào tham số ?id=</p>
    
    <?php
    if ($id) {
        $query = "SELECT username FROM users WHERE id = $id";

        $result = $db->exec($query); #cho phép stack query , nếu dùng query()->fail
        if ($result) {
            echo "<p style='color:green'>Thực thi thành công!</p>";
        } else {
            echo "<p style='color:red'>Lỗi: " . $db->lastErrorMsg() . "</p>";
        }
    }
    ?>
</body>
</html>