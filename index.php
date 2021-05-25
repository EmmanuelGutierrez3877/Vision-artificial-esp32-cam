<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
    <link rel="stylesheet" href="bootstrap.min.css">
</head>

<body>


    <?php 
        echo phpversion();
        ini_set('max_execution_time',0);
        //$conex = mysqli_connect("localhost","root","","Camara");
        $conex = mysqli_connect("sql10.freemysqlhosting.net","sql10414886","ezeL3RqZWt","sql10414886");

        while(1==1){
            $consulta = "SELECT * FROM `imagenes` ORDER BY `imagenes`.`fecha` DESC";
            $resultado = mysqli_query($conex,$consulta);
            $foto = $resultado->fetch_assoc();
        
    ?>



    <div id="foto" class="col-xs-11 col-sm-11 col-lg-7">
        <?php echo($foto['fecha']);
            echo $foto['imagen'];
            echo ('<img style="max-height: 100%; max-width: 100%;" src="data:image/jpeg;base64,'.base64_encode( $foto['imagen'] ).'"/>');
        ?>
    </div>


    <?php 
            while(1==1){
                sleep(0.5);
                $resultado2 = mysqli_query($conex,$consulta);
                $foto2 = $resultado2->fetch_assoc();

                if($foto2['id']!=$foto['id']){
                    $resultado = $resultado2;
                    ?>
                    <script>
                        var b = document.getElementById("foto");
                        b.parentNode.removeChild(b);
                    </script>
                    <?php
                    break;
                }
                
            }
    
        }
    
    ?>

</body>

</html>