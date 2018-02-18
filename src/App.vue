<template>
  <div id="app">
    <div class="container">
      <div class="number-container">
        <div class="number">{{ firstNumber }}</div>
      </div>
      <div class="number-container">
        <div class="times-sign">&times;</div>
        <div class="number">{{ secondNumber }}</div>
        <div class="bottom-line"></div>
      </div>
      <div class="answer-container">
        <div class="answer">
          <input type="number" class="form-control" v-model="answer">
        </div>
        <div class="submit-container">
          <button class="btn btn-lg btn-primary" @click="answer">Answer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
      firstNumber: 12,
      secondNumber: 8,
      answer: null
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.centered {
  text-align: center;
}

.number-container {
  margin: 0 auto;
  width: 100%;
  position: relative;
}

.number {
  font-size: 50px;
  width: 75px;
  text-align: right;
  margin: 0 auto;
}

.times-sign {
  position:absolute;
  left: calc(50% - 68px);
  font-size: 50px;
  bottom: 0px;
}

.bottom-line {
  position: absolute;
  border-bottom: 3px solid black;
  left: calc(50% - 68px);
  width:133px;
}

.answer-container {
  margin: 0 auto;
}

.answer {
  width: 110px;
  left: calc(50% - 56px);
  position: relative;
  margin-top: 10px;
  input {
    text-align: right;
    font-size: 50px;
    height: 60px;
    padding-right: 3px;
    margin-right: 0px;
    -moz-appearance:textfield;
  }
  input::-webkit-outer-spin-button,input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 10; /* <-- Apparently some margins are still there even though it's hidden */
  }
}

.submit-container {
  margin-top: 10px;
}

</style>
