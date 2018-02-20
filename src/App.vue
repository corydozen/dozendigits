<template>
  <div id="app">
    <div class="container">
      <div class="history-container">
        <div class="row" v-for="guess in history">
          <div class="col-12 alert" :class="{'alert-success': guess.correct, 'alert-danger': !guess.correct}">
            <span class="glyphicon glyphicon-ok-circle" aria-hidden="true" v-if="guess.correct"></span>
            <span class="glyphicon glyphicon-remove-circle" aria-hidden="true" v-if="!guess.correct"></span>
            <span>{{ guess.first_number + ' * ' + guess.second_number + ' = ' }}</span>
            <span :class="{'strikethrough': !guess.correct}">{{ guess.answer }}</span>
            <span v-if=!guess.correct>{{ parseInt(guess.first_number) * parseInt(guess.second_number) }}</span>
          </div>
        </div>
      </div>
    </div>
    <div class="difficulty-container">
      <div class="difficulty">
        <button class="btn" :class="{'btn-primary': difficulty=='low'}" @click.prevent="changeDifficulty('low')">Easy</button>
        <button class="btn" :class="{'btn-primary': difficulty=='medium'}" @click.prevent="changeDifficulty('medium')">Medium</button>
        <button class="btn" :class="{'btn-primary': difficulty=='high'}" @click.prevent="changeDifficulty('high')">Hard</button>
      </div>
    </div>
    <div class="number-container" v-if="!loading">
      <div class="number">{{ firstNumber }}</div>
    </div>
    <div class="number-container" v-if="!loading">
      <div class="times-sign">&times;</div>
      <div class="number">{{ secondNumber }}</div>
      <div class="bottom-line"></div>
    </div>
    <div class="answer-container" v-if="!loading">
      <div class="answer">
        <input id="answer" type="number" class="form-control" v-model="answer" @keyup.13="sendAnswer" :disabled="checking">
      </div>
      <div class="submit-container">
        <button class="btn btn-lg btn-primary" @click="sendAnswer" :disabled="checking">{{ checking ? 'Checking...' : 'Answer' }}</button>
      </div>
      <div class="alert-container">
        <div class="alert alert-success" v-if="alert.status == 'correct'">Correct!</div>
        <div class="alert alert-danger" v-if="alert.status == 'incorrect'">Incorrect</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import uuid from 'uuid';
import { baseurl } from '../config.js';
import Vue from 'vue';

export default {
  name: 'app',
  data () {
    return {
      loading: true,
      firstNumber: null,
      secondNumber: null,
      answer: null,
      userid: 1234,
      username: 1234,
      difficulty: 'low',
      alert: {
        id: null,
        status: null
      },
      alert_id: 0,
      checking: false,
      history: []
    }
  },
  mounted() {
    if(localStorage.getItem('userid')){
      this.userid = localStorage.getItem('userid');
    } else {
      this.userid = uuid.v4();
      localStorage.setItem('userid', this.userid);
    }
    this.getQuestion();
    this.getHistory();
  },
  methods: {
    getQuestion() {
      var self = this;
      axios.get(baseurl + '/answer?difficulty=' + this.difficulty)
        .then(({data}) => {
          self.firstNumber = data.first_number;
          self.secondNumber = data.second_number;
          self.loading = false;
        });
    },
    answerKeyDown(e) {
      console.log(e);
    },
    sendAnswer() {
      if (!this.checking) {
        var payload = {
          first_number: this.firstNumber,
          second_number: this.secondNumber,
          answer: this.answer,
          difficulty: this.difficulty,
          user_id: this.userid,
          username: this.username
        }
        var self = this;
        this.checking = true;
        axios.post(baseurl + '/answer', payload)
          .then(({data}) => {
            this.checking = false;
            var alert_id = self.alert_id++;
            self.alert.id = alert_id;
            if (data.correct) {
              self.alert.status = 'correct';
              self.firstNumber = data.next_question.first_number;
              self.secondNumber = data.next_question.second_number;
              self.answer = null;
              self.getHistory();
            } else {
              self.alert.status = 'incorrect';
              self.answer = null;
            }
            Vue.nextTick(() => {
              document.getElementById("answer").focus();
            });
            setTimeout(() => {
              if (self.alert.id === alert_id) {
                self.alert.id = null;
                self.alert.status = null;
              }
            }, 1500);
          });
      }
    },
    getHistory() {
      var self = this;
      axios.get(baseurl + '/history?userid=' + this.userid)
        .then(({data}) => {
          self.history = data;
        })
    },
    changeDifficulty(d) {
      this.difficulty = d;
      this.first_number = null;
      this.second_number = null;
      this.getQuestion();
    }
  }
}
</script>

<style lang="scss">
.history-container {
  position: absolute;
  .alert {
    text-align: left;
  }
}
.strikethrough {
  text-decoration: line-through;
}
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

.alert-container {
  margin-top: 10px;
  width: 200px;
  left: calc(50% - 100px);
  position: relative;
}

</style>
