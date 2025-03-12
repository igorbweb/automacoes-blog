<?php
if (ob_get_level() == 0) {
    ob_start();
}
set_time_limit(0);
ini_set('max_execution_time', 0);
ini_set('memory_limit', '512M');
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
/**
 * The template for displaying all single posts and attachments
 *
 * @package WordPress
 * @subpackage None Plate
 * @since None Plate 1.0
 */

get_header(); ?>

<style>
form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    justify-content: start;
    text-align: left;
    max-width: 800px;
    width: 100%;
    padding: 30px;
}

hr {
    border-top: 1px solid #ccc;
    height: 1px;
    width: 100%;
}

h1,
h4 {
    padding: 0;
    margin: 0;
}

p {
    margin: 0;
}

.console {
    padding: 20px;
    margin: 20px;
    border: 1px solid #ccc;
    max-height: 500px;
    overflow: auto;
}
</style>

<div id="content" class="reading reading-page">
    <form action="" method="POST" enctype="multipart/form-data">
        <h1>Importador 1.1</h1>
        <hr>
        <h4>Conexão:</h4>
        <input type="text" name="banco" placeholder="banco" id="banco" value="<?php echo (isset($_POST['banco']) ? $_POST['banco'] : '') ?>">
        <input type="text" name="usuario" placeholder="usuario" id="usuario" value="<?php echo (isset($_POST['usuario']) ? $_POST['usuario'] : '') ?>">
        <input type="text" name="senha" placeholder="senha" id="senha" value="<?php echo (isset($_POST['senha']) ? $_POST['senha'] : '') ?>">
        <input type="text" name="tabela" placeholder="Tabela" id="tabela" value="<?php echo (isset($_POST['tabela']) ? $_POST['tabela'] : '') ?>">
        <hr>
        <p>Ou selecione o arquivo JSON:<br><input type="file" name="arquivo" id="arquivo" accept="application/JSON" /></p>
        <hr>
        <h4>Campos:</h4>
        <input type="text" name="id" placeholder="ID" id="id" value="<?php echo (isset($_POST['id']) ? $_POST['id'] : '') ?>">
        <input type="text" name="titulo" placeholder="Coluna Título" id="titulo" value="<?php echo (isset($_POST['titulo']) ? $_POST['titulo'] : '') ?>">
        <input type="text" name="conteudo" placeholder="Coluna conteudo" id="conteudo" value="<?php echo (isset($_POST['conteudo']) ? $_POST['conteudo'] : '') ?>">
        <input type="text" name="imagem" placeholder="Coluna Imagem" id="imagem" value="<?php echo (isset($_POST['imagem']) ? $_POST['imagem'] : '') ?>">
        <input type="text" name="data" placeholder="Coluna Data" id="data" value="<?php echo (isset($_POST['data']) ? $_POST['data'] : '') ?>">
        <input type="text" name="localizacao" placeholder="Coluna Localizacao" id="localizacao" value="<?php echo (isset($_POST['localizacao']) ? $_POST['localizacao'] : '') ?>">
        <input type="text" name="url" placeholder="Base URL" id="url" value="<?php echo (isset($_POST['url']) ? $_POST['url'] : '') ?>">
        <p>Começar da linha: <input type="text" name="start" placeholder="Começar" id="start" value="<?php echo (isset($_POST['start']) ? $_POST['start'] : '1') ?>"></p>
        <hr>
        <p><input type="checkbox" name="testar" id="testar" <?php echo (isset($_POST['testar']) ? 'checked' : '') ?>> Testar query?</p>
        <input type="submit" value="Executar">
    </form>
    <div class="console">
        <strong>Console:<br></strong>
        <?php
        require_once(ABSPATH . 'wp-admin/includes/media.php');
        require_once(ABSPATH . 'wp-admin/includes/file.php');
        require_once(ABSPATH . 'wp-admin/includes/image.php');

        function insertPost($titulo, $conteudo, $data)
        {
            $my_post = array(
                'post_title'    => $titulo,
                'post_status'   => 'publish',
                'post_type'     => 'post',
                'post_content'  => $conteudo,
                'post_date' => $data
                
            );
            return wp_insert_post($my_post);
        }

        function getPostIdByTitle($titulo) {
            global $wpdb;
            return $wpdb->get_var($wpdb->prepare("SELECT ID FROM $wpdb->posts WHERE post_title = %s AND post_type = 'post'", $titulo));
        }
        
        function setPostThumbnailByUrl($post_id, $image_url) {
            if (!$post_id || empty($image_url)) return false;
            
            $image_id = media_sideload_image($image_url, $post_id, null, 'id');
            if (!is_wp_error($image_id)) {
                return set_post_thumbnail($post_id, $image_id);
            }
            return false;
        }
        
        if (!empty($_POST)) {
            if ($_FILES['arquivo']['name'] != "") {
                $upload_dir = dirname(__FILE__) . "/uploads/";
                $arquivo = $upload_dir . basename($_FILES['arquivo']['name']);
                
                if (move_uploaded_file($_FILES['arquivo']['tmp_name'], $arquivo)) {
                    $arquivoLido = json_decode(file_get_contents($arquivo), true);
                    
                    foreach ($arquivoLido as $dados) {
                        $titulo = $dados['titulo'] ?? '';
                        $imagem = $dados['imagem'] ?? '';
                        
                        if (!empty($titulo) && !empty($imagem)) {
                            $post_id = getPostIdByTitle($titulo);
                            
                            if ($post_id) {
                                if (setPostThumbnailByUrl($post_id, $imagem)) {
                                    echo "Thumbnail atualizada para: $titulo <br>";
                                } else {
                                    echo "Erro ao definir thumbnail para: $titulo <br>";
                                }
                            } else {
                                echo "Post não encontrado: $titulo <br>";
                            }
                        }
                    }
                } else {
                    echo "Erro ao fazer upload do arquivo.";
                }
            }
        }
        if (ob_get_level() == 0) {
            ob_end_flush();
        }
        ?>
    </div>
</div>
<?php get_footer(); ?>
