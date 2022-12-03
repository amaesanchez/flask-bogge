"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  gameId = response.data.game_id;
  let board = response.data.board;
  console.log("id", gameId, "resp", response)
  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty()
  let $tbody = $("<tbody>")

  for (let row of board) {
    let $trow = $("<tr>")
    for (let letter of row) {
      const $cell = $("<td>").text(letter)
      $trow.append($cell)
    }
    $tbody.append($trow)
  }

  $table.append($tbody)
}


start();

async function handleSubmit(evt) {
  evt.preventDefault();

  const word = $("#wordInput").val();
  let results = await sendPostRequestToAPI(gameId, word)

  if (!displayMessage(results)) {
    addWordToList(results, word)
  }

}

$(".word-input-btn").on("click", handleSubmit)

async function sendPostRequestToAPI(id, word) {
  let response = await axios.post("/api/score-word", {
    "game_id" : id,
    "word" : word
  })
  console.log("id", id)
  console.log("word", word)
  console.log("data", response.data)

  console.debug('sendPost ran')

  return response.data

}

function displayMessage(results) {
  if (results === { "result" : "not-word"} ||
    results === { "result" : "not-on-board"}) {
      $message.text("Not a legal play")
      return true
    }

  console.debug('display message ran')

  return false
}

function addWordToList(results, word) {
  $playedWords.append($(`<li>${word}</li>`))
  console.debug('addword ran')

}
