<template>
  <v-container class="fill-height">
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
                  <v-autocomplete label="Merkmalswert" :items="merksmalswerte" v-model="selectedMerkmalswert" @change="onSelectionChangeGetStartDatum"></v-autocomplete>
                  <v-autocomplete label="Startdatum" :items="startdatum" v-model="selectedStartdatum"></v-autocomplete>
                  <div>
                    <v-btn block :loading="loading" @click="getmw1">
                      Machine Learning Modell für Vorhersage initiieren
                      <template v-slot:loader>
                        <v-progress-linear color="red-darken-4" indeterminate></v-progress-linear>
                      </template>
                    </v-btn>
                  </div>
                </v-tab-item>

                <!-- Ähnlicher Aufbau für andere Tabs (G02, N02, N05, N08, P02) -->

              </v-tabs-items>
            </v-card-text>
          </v-card>
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
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({
    tab: 'B10',
    loading: false,
    mw1: {},
    merksmalswerte: [],
    startdatum: [],
    selectedMerkmalswert: null,
    selectedStartdatum: null,
  }),

  methods: {
    async fetchMerkmalswerte() {
      try {
        const { data } = await axios.get(`http://localhost:5000/get_merkmalswert/${this.tab}`);
        this.merksmalswerte = ['Alle Merkmalswerte', ...data]; // Hinzufügen von "Alle Merkmalswerte"
      } catch (error) {
        console.error('Fehler beim Abrufen der Merkmalswerte:', error);
      }
    },

    async onTabChange() {
      await this.fetchMerkmalswerte();
      this.selectedMerkmalswert = null; // Zurücksetzen des ausgewählten Merkmalswertes
    },

    async onSelectionChangeGetStartDatum(selectedItem) {
      try {
        const { data } = await axios.get(`http://localhost:5000/get_dates/${this.tab}/${this.selectedMerkmalswert}`);
        this.startdatum = data;
      } catch (error) {
        console.error('Fehler beim Abrufen der Startdaten:', error);
      }
    },

    async getmw1() {
      this.loading = true;
      try {
        const response = await axios.get('https://api.zippopotam.us/us/33162', {
          params: {
            merkmalswert: this.selectedMerkmalswert,
            startdatum: this.selectedStartdatum,
          },
        });
        this.mw1 = response.data;
      } catch (error) {
        console.error('Fehler beim Abrufen von mw1:', error);
      } finally {
        this.loading = false;
      }
    },
    
    // Ähnliche getmw Methoden für andere Tabs (getmw2, getmw3, etc.)

  },

  watch: {
    tab() {
      this.onTabChange();
    }
  },

  mounted() {
    this.fetchMerkmalswerte();
  }
};
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
