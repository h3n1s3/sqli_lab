<?php 
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
$host = "localhost";
$user = "root";
$pass = "";
$db_name = "mysql_rce";
$conn = new mysqli($host , $user , $pass);
if ($conn->connect_error) die("fail connect" . $conn->connect_error);

$conn->query("CREATE DATABASE IF NOT EXISTS $db_name");
$conn->select_db($db_name);

$sql_create = "CREATE TABLE IF NOT EXISTS users(
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    salary INT(10)
)";
$conn->query($sql_create);
$result = $conn->query("SELECT COUNT(*) as count from users");
$row = $result->fetch_assoc();

if ($row['count'] < 100){
    $conn->query("INSERT INTO users (username , password , salary) VALUES ('admin' , '123456' , 999999999) ");
    for ($i =2; $i <= 100; $i++){
        $u = "nhanvien" . $i;
        $p = "pass_" . $i;
        $s = rand(500,5000);
        $conn->query("INSERT INTO users(username , password , salary) VALUES ('$u' , '$p' , '$s')");

    }

}
$id = isset($_GET['id']) ? $_GET['id'] : '';
?>
<!DOCTYPE html>
<html>
    <head><title>BẢNG TRA CỨU NHÂN VIÊN</title></head>
    <body>
        <form method="GET">
            Staff ID : <input type="text" name="id" placeholder="input">
            <input type="submit" value="search">
        </form>
    </body>
</html>
<?php 
if ($id){
    $query = "SELECT * FROM users WHERE id = $id";
    $result = $conn->query($query);
    if ($result) {
            echo "<table border='1' cellpadding='10'>";
            echo "<tr><th>ID</th><th>Username</th><th>Salary</th></tr>";
            while($row = $result->fetch_assoc()) {
                echo "<tr>";
                echo "<td>" . $row["id"] . "</td>";
                echo "<td>" . $row["username"] . "</td>";
                echo "<td>" . $row["salary"] . "$</td>";
                echo "</tr>";
            }
            echo "</table>";
        } else {
            echo "<p style='color:red'>Lỗi SQL: " . $conn->error . "</p>";
        }
    }
?>

