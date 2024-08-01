<template>
  <v-container class="fill-height">
    <v-responsive
      class="align-centerfill-height mx-auto"
      max-width="955"
    >
      <v-img
        class="mt-4 mb-4"
        height="150"
        src="@/assets/logo.png"
      />

      <div class="text-center">
        <div class="text-body-2 font-weight-light mb-n1">Welcome to</div>

        <h1 class="text-h2 font-weight-bold">Machine Learning</h1>
      </div>

      <div class="py-4" />

      <v-row>
        <v-col cols="12">
          <v-card
            class="py-0"
            rounded="lg"
            variant="outlined"
          >
            
            <v-tabs
              v-model="tab"
              bg-color="grey-lighten-5"
              color="grey-darken-4"
              align-tabs="center"
              @input="onTabChange"
            >
              <v-tab value="B10">Einzugskanal</v-tab>
              <v-tab value="G02">Strohablage</v-tab>
              <v-tab value="N02">Fahrantrieb</v-tab>
              <v-tab value="N05">Triebachsbereifung</v-tab>
              <v-tab value="N08">Lenkachse</v-tab>
              <v-tab value="P02">Motorausführung</v-tab>
            </v-tabs>

            <v-card-text>
              <v-tabs-window v-model="tab">
                <v-tabs-window-item value="B10">
                <v-btn block
                      :loading="loading"
                      @click="onTabChange"
                    >
                      Initiate machine learning model for forecasting

                      <template v-slot:loader>
                        <v-progress-linear color="red-darken-4" indeterminate></v-progress-linear>
                      </template>
                    </v-btn>
                  <v-autocomplete
                    label="Merkmalswert"
                    :items="merksmalswerte"
                    v-model="selectedMerkmalswert"
                    @change="onSelectionChangeGetStartDatum"
                  ></v-autocomplete>
                  <v-autocomplete
                    label="Startdatum"
                    :items="startdatum"
                     v-model="selectedStartdatum"
                  ></v-autocomplete>
                  <div>
                    <v-btn block
                      :loading="loading"
                      @click="getmw1"
                    >
                      Initiate machine learning model for forecasting

                      <template v-slot:loader>
                        <v-progress-linear color="red-darken-4" indeterminate></v-progress-linear>
                      </template>
                    </v-btn>
                  </div >
                  
            
                </v-tabs-window-item>

                <v-tabs-window-item value="G02">
                  <v-autocomplete
                    label="Merkmalswert"
                    :items="merksmalswerte"
                    v-model="selectedMerkmalswert"
                    @change="onSelectionChangeGetStartDatum"
                  ></v-autocomplete>
                  <v-autocomplete
                    label="Startdatum"
                    :items="startdatum"
                     v-model="selectedStartdatum"
                  ></v-autocomplete>
                  <div>
                    <v-btn block
                      :loading="loading"
                      @click="getmw2"
                    >
                      Initiate machine learning model for forecasting

                      <template v-slot:loader>
                        <v-progress-linear color="red-darken-4" indeterminate></v-progress-linear>
                      </template>
                    </v-btn>
                  </div>
                </v-tabs-window-item>

                <v-tabs-window-item value="N02">
                  <v-autocomplete
                    label="Merkmalswert"
                    :items="merksmalswerte"
                    v-model="selectedMerkmalswert"
                    @change="onSelectionChangeGetStartDatum"
                  ></v-autocomplete>
                  <v-autocomplete
                    label="Startdatum"
                    :items="startdatum"
                     v-model="selectedStartdatum"
                  ></v-autocomplete>
                  <div>
                    <v-btn block
                      :loading="loading"
                      @click="getmw3"
                    >
                      Initiate machine learning model for forecasting

                      <template v-slot:loader>
                        <v-progress-linear color="red-darken-4" indeterminate></v-progress-linear>
                      </template>
                    </v-btn>
                  </div>
                </v-tabs-window-item>

                <v-tabs-window-item value="N05">
                  <v-autocomplete
                    label="Merkmalswert"
                    :items="merksmalswerte"
                    v-model="selectedMerkmalswert"
                    @change="onSelectionChangeGetStartDatum"
                  ></v-autocomplete>
                  <v-autocomplete
                    label="Startdatum"
                    :items="startdatum"
                     v-model="selectedStartdatum"
                  ></v-autocomplete>
                  <div>
                    <v-btn block
                      :loading="loading"
                      @click="getmw4"
                    >
                      Initiate machine learning model for forecasting

                      <template v-slot:loader>
                        <v-progress-linear color="red-darken-4" indeterminate></v-progress-linear>
                      </template>
                    </v-btn>
                  </div>

                  
                    <v-text>{{mw4}}</v-text>
                  
                    

                  
                </v-tabs-window-item>

                <v-tabs-window-item value="N08">
                  <v-autocomplete
                    label="Merkmalswert"
                    :items="merksmalswerte"
                    v-model="selectedMerkmalswert"
                    @change="onSelectionChangeGetStartDatum"
                  ></v-autocomplete>
                  <v-autocomplete
                    label="Startdatum"
                    :items="startdatum"
                     v-model="selectedStartdatum"
                  ></v-autocomplete>
                  <div>
                    <v-btn block
                      :loading="loading"
                      @click="getmw5"
                    >
                      Initiate machine learning model for forecasting

                      <template v-slot:loader>
                        <v-progress-linear color="red-darken-4" indeterminate></v-progress-linear>
                      </template>
                    </v-btn>
                  </div>
                  <v-text v-if="mw5">{{mw5}}</v-text>
                </v-tabs-window-item>

                <v-tabs-window-item value="P02">
                  <v-autocomplete
                    label="Merkmalswert"
                    :items="merksmalswerte"
                    v-model="selectedMerkmalswert"
                    @change="onSelectionChangeGetStartDatum"
                  ></v-autocomplete>
                  <v-autocomplete
                    label="Startdatum"
                    :items="startdatum"
                     v-model="selectedStartdatum"
                  ></v-autocomplete>
                  <div>
                    <v-btn block
                      :loading="loading"
                      @click="getmw6"
                    >
                      Initiate machine learning model for forecasting

                      <template v-slot:loader>
                        <v-progress-linear color="red-darken-4" indeterminate></v-progress-linear>
                      </template>
                    </v-btn>
                  </div>
                </v-tabs-window-item>
              </v-tabs-window>
            </v-card-text>

          </v-card>
        </v-col>
      </v-row>
      <v-row class="mb-16">
        <v-col cols="12">
          <v-expansion-panels>
            <v-expansion-panel rounded="lg" variant="outlined" >
            <v-expansion-panel-title class="text-h6">
           What are the Option Take Rates?
            </v-expansion-panel-title>
            <v-expansion-panel-text>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</v-expansion-panel-text>
              </v-expansion-panel>
            <v-expansion-panel rounded="lg" variant="outlined" >
            <v-expansion-panel-title class="text-h6">
            How to predict for the next month?
            </v-expansion-panel-title>
            <v-expansion-panel-text>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</v-expansion-panel-text>
              </v-expansion-panel>
            <v-expansion-panel rounded="lg" variant="outlined" >
            <v-expansion-panel-title class="text-h6">
           How to change the value?
            </v-expansion-panel-title>
            <v-expansion-panel-text>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</v-expansion-panel-text>
              </v-expansion-panel>
          </v-expansion-panels>
        </v-col>
      </v-row>
    </v-responsive>
  </v-container>
</template>

<script>
  import axios from "axios";
  
  export default {
    data: () => ({
      tab: "B10",
      loading: false,
      mw1: {},
      mw2: {},
      mw3: {},
      mw4: {},
      mw5: {},
      mw6: {},
      merksmalswerte: ['Merkmalswert 1', 'Merkmalswert 2','Merkmalswert 3','Merkmalswert 4'],
      startdatum: ['Startdatum 1', 'Startdatum 2','Startdatum 3','Startdatum 4'],
      selectedMerkmalswert: null,
      selectedStartdatum: null,
    }),

    methods: {

      async onTabChange() {
        console.log("ahahaha");
        const { data } = await axios.get(`http://localhost:5000/get_merkmalswert/${this.tab}`);
        this.merksmalswerte = data;  
      },

      async onSelectionChangeGetStartDatum(selectedItem){
        const { data } = await axios.get(`http://localhost:5000/get_dates/${this.tab}/${selectedMerkmalswert}`);
        this.startdatum = data; 
      },
      
      async getmw1() {
        const response = await           axios.get("https://api.zippopotam.us/us/33162", {
          params: {
            merkmalswert: this.selectedMerkmalswert,
            startdatum: this.selectedStartdatum
          }
        });
        this.mw1 = response.data;
      },

      async getmw2() {
        const { data } = await axios.get("https://yesno.wtf/api");
        this.mw2 = data;
      },

      async getmw3() {
        const { data } = await axios.get("https://yesno.wtf/api");
        this.mw3 = data;
      },

      async getmw4() {
        const { data } = await axios.get("https://yesno.wtf/api");
        this.mw4 = data;
      },

      async getmw5() {
        const { data } = await axios.get("https://yesno.wtf/api");
        this.mw5 = data;
      },

      async getmw6() {
        const { data } = await axios.get("https://yesno.wtf/api");
        this.mw6 = data;
      },
    },
    
    computed: {
      virtualBoats () {
        return [...Array(10000).keys()].map(i => {
          const boat = { ...this.boats[i % this.boats.length] }
          boat.name = `${boat.name} #${i}`
          return boat
        })
      },
    },
    
    watch: {
      loading (val) {
        if (!val) return

        setTimeout(() => (this.loading = false), 2000)
      },
    },
  }
</script>

<style>
.custom-panel {
  margin-bottom: 16px; /* Beispiel für benutzerdefinierte Styles */
  border: 1px solid #ccc;
  border-radius: 8px;
  opacity: 0.9; /* Beispiel für Opacity-Wert */
}

.custom-title {
   font-size: 120px; /* Beispiel für größere Schriftgröße */
}


</style>
