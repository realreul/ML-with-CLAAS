<template>
  <v-app>
    <v-main>
      <v-container fluid fill-height class="background">
        <div class="overlay"></div>
        <HelloWorld />
      </v-container>
    </v-main>

    <AppFooter />
  </v-app>
</template>

<script setup>
  //
</script>

<style>
.background {
    position: relative;
    overflow: hidden;
    height: 100vh; /* Stellt sicher, dass der Container die volle Höhe einnimmt */
    background-image: url('@/assets/claas-xerion-terra-trac.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
  }

.overlay {
   position: absolute;
   top: 0;
   left: 0;
   width: 100%;
   height: 100%;
   background: rgba(0, 0, 0, 0.5); /* Stellt die Overlay-Farbe und Transparenz ein */
   z-index: 0; /* Stellt sicher, dass die Überlagerung hinter dem Inhalt liegt */
}
  
</style>