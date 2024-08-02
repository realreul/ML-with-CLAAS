<template>
  <v-container class="fill-height" fluid>
    <v-row class="fill-height">
      <v-col>
        <v-responsive class="align-center fill-height mx-auto" max-width="955">
          <v-img class="mt-4 mb-4" height="150" src="@/assets/logo.png" />

          <div class="text-center">
            <div class="text-body-2 font-weight-light mb-n1">Willkommen zu</div>
            <h1 class="text-h2 font-weight-bold">Machine Learning</h1>
          </div>

          <div class="py-4" />

          <v-row>
            <v-col cols="12">
              <v-card class="py-0" rounded="lg" variant="outlined">
                <v-tabs v-model="tab" bg-color="grey-lighten-5" color="grey-darken-4" align-tabs="center" @change="onTabChange">
                  <v-tab value="B10">Einzugskanal</v-tab>
                  <v-tab value="G02">Strohablage</v-tab>
                  <v-tab value="N02">Fahrantrieb</v-tab>
                  <v-tab value="N05">Triebachsbereifung</v-tab>
                  <v-tab value="N08">Lenkachse</v-tab>
                  <v-tab value="P02">Motorausführung</v-tab>
                </v-tabs>

                <v-card-text>
                  <v-tabs-items v-model="tab">
                    <v-tab-item value="B10">
                      <v-select
                        label="Merkmalswert"
                        :items="merksmalswerte"
                        v-model="selectedMerkmalswert"
                        @update:modelValue="onSelectionChangeGetStartDatum"
                      ></v-select>
                      <v-select
                        label="Startdatum"
                        :items="startdatum"
                        v-model="selectedStartdatum"
                      ></v-select>

                      <!-- Radio Buttons hinzugefügt -->
                      <v-radio-group v-model="selectedOption" row>
                        <v-radio label="OptionTakeRate" value="optionTakeRate"></v-radio>
                        <v-radio label="Gesamte Anzahl" value="gesamteAnzahl"></v-radio>
                      </v-radio-group>
                      
                      <div>
                        <v-btn block :loading="loading" @click="getmw1">
                          Machine Learning Modell für Vorhersage initiieren
                          <template v-slot:loader>
                            <v-progress-linear color="red-darken-4" indeterminate></v-progress-linear>
                          </template>
                        </v-btn>
                      </div>
                    </v-tab-item>
                    <!-- Ähnlicher Aufbau für andere Tabs -->
                  </v-tabs-items>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Tabelle zur Anzeige der Vorhersagedaten -->
          <v-row class="mb-16">
            <v-col cols="12">
              <v-simple-table v-if="mw1.length > 0 && selectedMerkmalswert !== 'Alle Merkmalswerte'" class="prediction-table">
                <thead>
                  <tr>
                    <th v-for="(item, index) in mw1" :key="'date-header-' + index">{{ item[0] }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td v-for="(item, index) in mw1" :key="'value-' + index">{{ item[1] }}</td>
                  </tr>
                </tbody>
              </v-simple-table>
            </v-col>
          </v-row>
          
          <v-row class="mb-16">
            <v-col cols="12">
              <v-expansion-panels>
                <v-expansion-panel rounded="lg" variant="outlined">
                  <v-expansion-panel-title class="text-h6">Was sind die Optionsannahmeraten?</v-expansion-panel-title>
                  <v-expansion-panel-text>Lorem ipsum...</v-expansion-panel-text>
                </v-expansion-panel>
                <v-expansion-panel rounded="lg" variant="outlined">
                  <v-expansion-panel-title class="text-h6">Wie sagt man den nächsten Monat vorher?</v-expansion-panel-title>
                  <v-expansion-panel-text>Lorem ipsum...</v-expansion-panel-text>
                </v-expansion-panel>
                <v-expansion-panel rounded="lg" variant="outlined">
                  <v-expansion-panel-title class="text-h6">Wie ändert man den Wert?</v-expansion-panel-title>
                  <v-expansion-panel-text>Lorem ipsum...</v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-col>
          </v-row>
        </v-responsive>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({
    tab: 'B10',
    loading: false,
    mw1: [], // Von {} zu [] geändert
    merksmalswerte: [],
    startdatum: [],
    selectedMerkmalswert: null,
    selectedStartdatum: null,
    selectedOption: 'optionTakeRate', // Neue Datenbindung für Radio-Buttons
  }),

  methods: {
    async fetchMerkmalswerte() {
      try {
        console.log('fetchMerkmalswerte: Start fetching merksmalswerte');
        const { data } = await axios.get(`http://localhost:5000/get_merkmalswert/${this.tab}`);
        this.merksmalswerte = ['Alle Merkmalswerte', ...data];
        console.log('fetchMerkmalswerte: Data fetched successfully', this.merksmalswerte);
      } catch (error) {
        console.error('Fehler beim Abrufen der Merkmalswerte:', error);
      }
    },

    async onTabChange() {
      console.log('onTabChange: Tab changed to', this.tab);
      this.selectedMerkmalswert = null;
      this.selectedStartdatum = null;
      this.mw1 = []; // Setze mw1 zurück
      await this.fetchMerkmalswerte();
    },

    async onSelectionChangeGetStartDatum(item) {
      console.log('onSelectionChangeGetStartDatum: Selected Merkmalswert', item);
      this.selectedStartdatum = null; // Setze das Datumsfeld zurück
      if (item) {
        try {
          console.log('onSelectionChangeGetStartDatum: Start fetching startdatum');
          const { data } = await axios.get(`http://localhost:5000/get_dates/${this.tab}/${item}`);
          this.startdatum = data;
          console.log('onSelectionChangeGetStartDatum: Startdatum fetched successfully', this.startdatum);
        } catch (error) {
          console.error('Fehler beim Abrufen der Startdaten:', error);
        }
      }
    },

    async getmw1() {
      this.loading = true;
      console.log('getmw1: Start fetching mw1');
      try {
        const response = await axios.post('http://localhost:5000/predict', {
          merkmal: this.tab,
          merkmalswert: this.selectedMerkmalswert,
          startdatum: this.selectedStartdatum,
          zielvariable: this.selectedOption // Neue Option hinzugefügt
        }, { responseType: 'blob' }); // Antworttyp auf 'blob' setzen

        if (this.selectedMerkmalswert === "Alle Merkmalswerte") {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'predictions.csv');
          document.body.appendChild(link);
          link.click();
          window.URL.revokeObjectURL(url);
        } else {
          const textData = await response.data.text();
          this.mw1 = JSON.parse(textData); // Speichert die empfangenen Daten in mw1
          console.log('getmw1: Data fetched successfully', this.mw1);
        }
      } catch (error) {
        console.error('Fehler beim Abrufen von mw1:', error);
      } finally {
        this.loading = false;
        console.log('getmw1: Finished fetching mw1');
      }
    },
  },

  watch: {
    tab() {
      this.onTabChange();
    },
    selectedMerkmalswert() {
      this.mw1 = []; // Setze mw1 zurück
    },
    selectedStartdatum() {
      this.mw1 = []; // Setze mw1 zurück
    }
  },

  mounted() {
    console.log('Component mounted: Start fetching merksmalswerte');
    this.fetchMerkmalswerte();
  }
};
</script>


<style>
.custom-panel {
  margin-bottom: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
  opacity: 0.9;
}

.custom-title {
  font-size: 120px;
}

.prediction-table {
  margin-top: 16px;
  border-collapse: collapse;
  width: 100%;
}

.prediction-table th, .prediction-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}

.prediction-table th {
  background-color: #f2f2f2;
  color: #424242;
  font-family: "Roboto", sans-serif; /* Schriftart hinzugefügt */
}

.prediction-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.fill-height {
  height: 100vh;
}

.overflow-auto {
  overflow: auto;
}
</style>
