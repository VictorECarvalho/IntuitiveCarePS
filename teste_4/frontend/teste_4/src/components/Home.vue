<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/minty/bootstrap.min.css" integrity="sha384-H4X+4tKc7b8s4GoMrylmy2ssQYpDHoqzPa9aKXbDwPoPUA3Ra8PA5dGzijN+ePnH" crossorigin="anonymous">
      <div class="row">
        <div class="col-sm-12">
          <h1 class="text-center bg-primary text-white" style="border-radius: 10px;">Consulta de Operadoras</h1>
          <hr><br>
          <button type="button" class="btn btn-success btn-bg" v-b-modal.filtro-modal>Buscar</button>
          <br><br>
          <a class="text-center" v-if="filtro.col != '' && filtro.val != ''">
            Filtro: {{ filtro.col }} = {{ filtro.val }}
          </a>
          <br><br>
          <div class="scrollable text-center green flex-grow-1 flex-shrink-0 overflow-x-scroll overflow-y-scroll" style="width: 100%; height:700px;">

            <table sticky-header class="table table-hover sticky-header">
              <thead style="position:sticky;"> 
                <tr>
                  <th v-for="(col, index) in cols" :key="index">{{ col }}</th>
                </tr>
              </thead>  
              <tbody>
                <tr v-for="(row, index) in filteredRows" :key="index">
                  <td>{{ row.Registro_ANS }}</td>
                  <td>{{ row.CNPJ }}</td>
                  <td>{{ row.Razao_Social }}</td>
                  <td>{{ row.Nome_Fantasia }}</td>
                  <td>{{ row.Modalidade }}</td>
                  <td>{{ row.Logradouro }}</td>
                  <td>{{ row.Numero }}</td>
                  <td>{{ row.Complemento }}</td>
                  <td>{{ row.Bairro }}</td>
                  <td>{{ row.Cidade }}</td>
                  <td>{{ row.UF }}</td>
                  <td>{{ row.CEP }}</td>
                  <td>{{ row.DDD }}</td>
                  <td>{{ row.Telefone }}</td>
                  <td>{{ row.Fax }}</td>
                  <td>{{ row.Endereco_eletronico }}</td>
                  <td>{{ row.Representante }}</td>
                  <td>{{ row.Cargo_Representante }}</td>
                  <td>{{ row.Regiao_de_Comercializacao }}</td>
                  <td>{{ row.Data_Registro_ANS }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          </div>
        </div>
      </div>

      <b-modal ref="filtroModal"
        id="filtro-modal"
        title="Filtrar tabela" hide-backdrop hide-footer>
        <b-form class="w-100">
        <b-form-group id="form-atribute-group"
          label="Atributo"
          label-for="form-atribute-input">
          <b-form-select
            id="form-atribute-input"
            v-model="filtro.col"
            :options="cols"
            required
            placeholder="Selecione um atributo">
          </b-form-select>
        </b-form-group>
        <b-form-group id="form-value-group"
          label="Valor"
          label-for="form-value-input">
          <b-form-input
            id="form-value-input"
            v-model="filtro.val"
            type="text"
            required
            placeholder="Digite o valor">
          </b-form-input>
        </b-form-group>
        <b-button type="clear" variant="primary">Buscar</b-button>
        </b-form>
      </b-modal>
  </div>
  <!--First Model-->



</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      rows: [],
      status: "",
      cols: [],
      filteredCols: [],
      numOfColumns: 0,
      filtro:{
        col: "",
        val: ""
      }
    };
  },
  methods: {
    getData(){
      const path = 'http://localhost:5000/get_data';
      axios.get(path)
        .then((response) => {
          console.log(response.data.status);
          this.status = response.data.status; 
          this.rows = response.data.data;
          this.cols = response.data.columns;
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    },
    initFilter() {
      this.filtro.col = "";
      this.filtro.val = "";
    },

  },
    created() {
      this.getData();
    },
    computed: {
      filteredRows:function() {
        if (this.filtro.col != "" && this.filtro.val != "") {
          return this.rows.filter((row) => {
            return row[this.filtro.col].toString().toLowerCase().match(this.filtro.val.toLowerCase());
          });
        }
        return this.rows;
      }
    },
  };
</script>
