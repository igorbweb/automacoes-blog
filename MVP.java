import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class MVP {

    public static void main(String[] args) {
        Sistema sistema = new Sistema();

        Pessoa pessoa1 = new Pessoa("João", "123456789", "Masculino", new Date(), "Rua A", 0);
        Pessoa pessoa2 = new Pessoa("Maria", "987654321", "Feminino", new Date(), "Rua B", 0);

        Veiculo veiculo1 = new Veiculo("Azul", "Ford", "Focus", "SE", "123456789", "XYZ1234", 2020, 2020, true, false);
        Veiculo veiculo2 = new Veiculo("Vermelho", "Chevrolet", "Cruze", "LT", "987654321", "ABC5678", 2019, 2019, false, true);

        sistema.cadastrarPessoa(pessoa1);
        sistema.cadastrarPessoa(pessoa2);

        sistema.cadastrarVeiculo(veiculo1);
        sistema.cadastrarVeiculo(veiculo2);

        List<Pessoa> pessoas = sistema.listarPessoas();
        List<Veiculo> veiculos = sistema.listarVeiculos();

        System.out.println("Pessoas cadastradas:");
        for (Pessoa pessoa : pessoas) {
            System.out.println(pessoa);
        }

        System.out.println("\nVeículos cadastrados:");
        for (Veiculo veiculo : veiculos) {
            System.out.println(veiculo);
        }
    }
}

class Sistema {
    private List<Pessoa> pessoas;
    private List<Veiculo> veiculos;

    public Sistema() {
        this.pessoas = new ArrayList<>();
        this.veiculos = new ArrayList<>();
    }

    public void cadastrarPessoa(Pessoa pessoa) {
        pessoas.add(pessoa);
    }

    public void cadastrarVeiculo(Veiculo veiculo) {
        veiculos.add(veiculo);
    }

    public List<Pessoa> listarPessoas() {
        return pessoas;
    }

    public List<Veiculo> listarVeiculos() {
        return veiculos;
    }
}

class Pessoa {
    public String Nome;
    private String Documento;
    public String Sexo;
    private Date DataNascimento;
    public String Endereco;
    public int IndiceRoubo;

    public Pessoa(String nome, String documento, String sexo, Date dataNascimento, String endereco, int indiceRoubo) {
        this.Nome = nome;
        this.Documento = documento;
        this.Sexo = sexo;
        this.DataNascimento = dataNascimento;
        this.Endereco = endereco;
        this.IndiceRoubo = indiceRoubo;
    }

    // Outros métodos podem ser adicionados aqui, como getters e setters.
    
    @Override
    public String toString() {
        return "Nome: " + Nome + ", Documento: " + Documento + ", Sexo: " + Sexo + ", Endereco: " + Endereco;
    }
}

class Veiculo {
    public String Cor;
    public String Fabricante;
    public String Modelo;
    public String Versao;
    private String Chassi;
    private String Placa;
    public int AnoFabricacao;
    public int AnoModelo;
    private Boolean UnicoDono;
    private Boolean SofreuSinistro;

    public Veiculo(String cor, String fabricante, String modelo, String versao, String chassi, String placa,
                   int anoFabricacao, int anoModelo, Boolean unicoDono, Boolean sofreuSinistro) {
        this.Cor = cor;
        this.Fabricante = fabricante;
        this.Modelo = modelo;
        this.Versao = versao;
        this.Chassi = chassi;
        this.Placa = placa;
        this.AnoFabricacao = anoFabricacao;
        this.AnoModelo = anoModelo;
        this.UnicoDono = unicoDono;
        this.SofreuSinistro = sofreuSinistro;
    }

    // Outros métodos podem ser adicionados aqui, como getters e setters.

    @Override
    public String toString() {
        return "Modelo: " + Modelo + ", Placa: " + Placa + ", Ano de Fabricação: " + AnoFabricacao;
    }
}
