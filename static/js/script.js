// reformat the code below
const button1 = document.querySelector("#btn1");
const button2 = document.querySelector("#btn2");
const button3 = document.querySelector("#btn3");
const button4 = document.querySelector("#btn4");
const button5 = document.querySelector("#btn5");
const button6 = document.querySelector("#btn6");
const canvasItem = document.querySelector("#canvas");
const get_p = document.querySelector("#get_id");
const lang = document.querySelector("#get_lang").textContent;
console.log(lang);
const current_id = get_p.textContent;
const buttonNext = document.querySelector("#btnNext");
const buttonPrev = document.querySelector("#btnPrev");
const submitButton = document.querySelector("#submit");
const showAllSamples = document.querySelector("#showall");
let counter = 0;
let poly_counter = 0;
let label = "";
const allDivs = document.querySelectorAll("div.d-flex.justify-content-evenly");
const negativeTagsRadios = document
  .querySelectorAll("div.row.align-items-center.mt-5.justify-content-center")[0]
  .querySelectorAll("input");
const positiveTagsRadios = document
  .querySelectorAll("div.row.align-items-center.mt-5.justify-content-center")[1]
  .querySelectorAll("input");

allDivs.forEach((radioButton) => {
  radioButton.addEventListener("click", function () {
    if (!this.clicked) {
      counter++;
      this.clicked = true;
    }
  });
});
let negative_tag_counter = 0;
negativeTagsRadios.forEach((radioButton) => {
  radioButton.addEventListener("click", function () {
    negative_tag_counter++;
    let sample_id = this.id.substring(0, this.id.length - 1);
    if (this.id.includes("/")) {
      sample_id = sample_id.replace("/", "");
    }
    sample_id = sample_id.replace(" ", "");
    sample_id = sample_id.toLowerCase();
    label = sample_id + "_neg";

    if (!this.clicked) {
      this.clicked = true;
    }
  });
});
let positive_tag_counter = 0;
positiveTagsRadios.forEach((radioButton) => {
  radioButton.addEventListener("click", function () {
    positive_tag_counter++;
    let sample_id = this.id;
    if (this.id.includes("/")) {
      sample_id = sample_id.replace("/", "");
    }
    sample_id = sample_id.replace(" ", "");
    sample_id = sample_id.toLowerCase();
    label = sample_id;
    if (!this.clicked) {
      this.clicked = true;
    }
  });
});
var r = document.querySelector(":root");
color_dict = {
  primary: "#2f35fa",
  danger: "#f52003",
  success: "#08ae66",
  dark: "#000000",
};
const theme = button1.classList[1].split("-")[1];
r.style.setProperty("--range_slider", color_dict["dark"]);
r.style.getP;

const allRanges = document.querySelectorAll(".range-wrap");
allRanges.forEach((wrap) => {
  const range = wrap.querySelector(".form-range");
  const bubble = wrap.querySelector(".bubble");
  bubble.classList.add("bg-dark");
  range.addEventListener("input", () => {
    setBubble(range, bubble);
  });
  setBubble(range, bubble);
});
let positive_samples = [];
let negative_samples = [];
// Functions are hoisted in JavaScript unless the strict JavaScript is used. Thefore you can define functions you use in your code after the code that uses them.
function setBubble(range, bubble) {
  const val = range.value;
  const min = range.min ? range.min : 0;
  const max = range.max ? range.max : 100;
  const newVal = Number(((val - min) * 100) / (max - min));
  bubble.innerHTML = val;
  // Sorta magic numbers based on size of the native UI thumb
  bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.15}px))`;
  bubble.style.top = `1.3rem`;
}

const formList = document.querySelector(".carousel-inner");
const carouselItems = formList.querySelectorAll(".carousel-item");
// remove all carousel items active class and active class
const button_list = [
  button1,
  button2,
  button3,
  button4,
  button5,
  button6,
];
button1.addEventListener("click", (e) => {
  e.preventDefault();
  // First remove from others
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list.map((button) => button.classList.add("btn-outline-" + theme));
  // Add primary now
  button1.classList.add("btn-" + theme);
  button1.classList.remove("btn-outline-" + theme);
  buttonNext.classList.remove("d-none");
  carouselItems.forEach((elem) => elem.classList.remove("active"));
  carouselItems[0].classList.add("active");
  buttonPrev.classList.add("d-none");
});
button2.addEventListener("click", (e) => {
  e.preventDefault();
  // First remove from others
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list.map((button) => button.classList.add("btn-outline-" + theme));
  // Add primary now
  button2.classList.add("btn-" + theme);
  button2.classList.remove("btn-outline-" + theme);
  buttonPrev.classList.remove("d-none");
  carouselItems.forEach((elem) => elem.classList.remove("active"));
  buttonNext.classList.remove("d-none");
  carouselItems[1].classList.add("active");
});
button3.addEventListener("click", (e) => {
  e.preventDefault();
  // First remove from others
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list.map((button) => button.classList.add("btn-outline-" + theme));
  // Add primary now
  button3.classList.add("btn-" + theme);
  buttonPrev.classList.remove("d-none");
  button3.classList.remove("btn-outline-" + theme);
  carouselItems.forEach((elem) => elem.classList.remove("active"));
  buttonNext.classList.remove("d-none");
  carouselItems[2].classList.add("active");
});
button4.addEventListener("click", (e) => {
  e.preventDefault();
  // First remove from others
  buttonPrev.classList.remove("d-none");
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list.map((button) => button.classList.add("btn-outline-" + theme));
  // Add primary now
  button4.classList.add("btn-" + theme);
  button4.classList.remove("btn-outline-" + theme);
  carouselItems.forEach((elem) => elem.classList.remove("active"));
  buttonNext.classList.remove("d-none");
  carouselItems[3].classList.add("active");
});
button5.addEventListener("click", (e) => {
  e.preventDefault();
  // First remove from others
  buttonPrev.classList.remove("d-none");
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list.map((button) => button.classList.add("btn-outline-" + theme));
  // Add primary now
  button5.classList.add("btn-" + theme);
  button5.classList.remove("btn-outline-" + theme);
  carouselItems.forEach((elem) => elem.classList.remove("active"));
  buttonNext.classList.remove("d-none");
  carouselItems[4].classList.add("active");
});
button6.addEventListener("click", (e) => {
  e.preventDefault();
  // First remove from others
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list.map((button) => button.classList.add("btn-outline-" + theme));
  // Add primary now
  button6.classList.add("btn-" + theme);
  button6.classList.remove("btn-outline-" + theme);
  buttonPrev.classList.remove("d-none");
  buttonNext.classList.remove("d-none");
  carouselItems.forEach((elem) => elem.classList.remove("active"));
  carouselItems[5].classList.add("active");
  submitButton.classList.remove("d-none");
  buttonNext.classList.add("d-none");
  buttonPrev.classList.remove("d-none");
});
buttonNext.addEventListener("click", (e) => {
  let active = document.querySelector(".carousel-item.active");
  // Get its ID
  e.preventDefault();
  let active_id = active.id;

  carouselItems.forEach((elem) => elem.classList.remove("active"));
  carouselItems[active_id - 1].classList.add("active");
  button_list.map((button) => button.classList.add("btn-outline-" + theme)); // add all btn-outline
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list[active_id].classList.remove("btn-outline-" + theme);
  button_list[active_id].classList.add("btn-" + theme);
  buttonPrev.classList.remove("d-none");
  let next = active.nextElementSibling;
  if (next) {
    active.classList.remove("active");
    next.classList.add("active");
  }
  if (active_id == 5) {
    submitButton.classList.remove("d-none");
    buttonNext.classList.add("d-none");
    return;
  }
});
buttonPrev.addEventListener("click", (e) => {
  e.preventDefault();
  let active = document.querySelector(".carousel-item.active");
  // Get its ID

  let active_id = active.id;
  if (active_id == 1) {
    buttonPrev.classList.add("d-none");
    return;
  }
  carouselItems.forEach((elem) => elem.classList.remove("active"));
  carouselItems[active_id - 2].classList.add("active");
  button_list.map((button) => button.classList.add("btn-outline-" + theme)); // add all btn-outline
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list[active_id - 2].classList.remove("btn-outline-" + theme);
  button_list[active_id - 2].classList.add("btn-" + theme);
  let prev = active.previousElementSibling;
  if (prev) {
    active.classList.remove("active");
    prev.classList.add("active");
  }
  buttonNext.classList.remove("d-none");
});
// Draw polygons with the following code
// https://stackoverflow.com/questions/29441389/how-to-draw-polygon-on-canvas-with-mouse-clicks-pure-js
// JQuery Code
submitButton.addEventListener("click", (e) => {
  e.preventDefault();
  // hiç etiketlenmemişse geç
  console.log(counter);
 if (counter > 0 && counter < 24 ) {
    if (lang == "en") alert("Please fill in all the fields.");
    else alert("Lütfen tüm alanları doldurun.");
    return;
  }
  if (lang == "en") alert("Your data is saved. Thank you.");
  else alert("Etiketleme işlemi tamamlandı");
  let fields = $(":input").serializeArray();
  fields.positive_samples = positive_samples;
  fields.negative_samples = negative_samples;
  $.post(
    "/postmethod",
    {
      jsdata: JSON.stringify(fields),
      negative_samples: JSON.stringify(negative_samples),
      positive_samples: JSON.stringify(positive_samples),
      image_id: current_id,
      language: lang,
    },
    function (data) {
       window.location = data;
    }
  );
});
var canvas = document.getElementById("canvas");
let context = canvas.getContext("2d");
context.strokeStyle = "#FF0000";
var cw = canvas.width;
var ch = canvas.height;
function reOffset() {
  var BB = canvas.getBoundingClientRect();
  offsetX = BB.left;

  offsetY = BB.top;
}
var offsetX, offsetY;
reOffset();
window.onscroll = function (e) {
  reOffset();
};

context.lineWidth = 2;
context.strokeStyle = "blue";

let coordinates = [];

$("#positives").click(function (e) {
  e.preventDefault();
  if (poly_counter == 0) {
    if (lang == "en") alert("Please draw a polygon first.");
    else alert("Lütfen önce bir şekil çizin.");
    return;
  }
  if (positive_tag_counter == 0) {
    if (lang == "en") alert("Please select a positive tag first.");
    else alert("Lütfen önce pozitif bir etiket seçin.");

    return;
  }
  positiveTagsRadios.forEach((radioButton) => {
    radioButton.checked = false;
  });
  if (lang == "en") alert("Positive sample added.");
  else alert("Pozitif örnek eklendi.");
  positive_tag_counter = 0;
  coordinates.push({ label: label });
  positive_samples.push(coordinates);
  // Draw positive samples on the canvas
  coordinates = [];
  context.clearRect(0, 0, cw, ch);
  context.lineWidth = 4;
  context.strokeStyle = "green";
  context.fillStyle = "rgba(0,255,0,.2)";
  for (var i = 0; i < positive_samples.length; i++) {
    context.beginPath();
    context.moveTo(positive_samples[i][0].x, positive_samples[i][0].y);
    for (var j = 1; j < positive_samples[i].length; j++) {
      context.lineTo(positive_samples[i][j].x, positive_samples[i][j].y);
    }

    context.closePath();
    context.fill();
    context.stroke();
  }
  context.strokeStyle = "red";
  context.fillStyle = "rgba(255,0,0,.2)";
  for (var i = 0; i < negative_samples.length; i++) {
    context.beginPath();
    context.moveTo(negative_samples[i][0].x, negative_samples[i][0].y);
    for (var j = 1; j < negative_samples[i].length; j++) {
      context.lineTo(negative_samples[i][j].x, negative_samples[i][j].y);
    }

    context.closePath();
    context.fill();
    context.stroke();
  }
  poly_counter = 0;
  // Fetch the pressed text
});
$("#showall").click(function (e) {
  e.preventDefault();
  context.lineWidth = 4;
  context.strokeStyle = "green";
  context.fillStyle = "rgba(0,255,0,.2)";
  for (var i = 0; i < positive_samples.length; i++) {
    context.beginPath();
    context.moveTo(positive_samples[i][0].x, positive_samples[i][0].y);
    for (var j = 1; j < positive_samples[i].length; j++) {
      context.lineTo(positive_samples[i][j].x, positive_samples[i][j].y);
    }

    context.closePath();
    context.fill();
    context.stroke();
  }
  context.strokeStyle = "red";
  context.fillStyle = "rgba(255,0,0,.2)";
  for (var i = 0; i < negative_samples.length; i++) {
    context.beginPath();
    context.moveTo(negative_samples[i][0].x, negative_samples[i][0].y);
    for (var j = 1; j < negative_samples[i].length; j++) {
      context.lineTo(negative_samples[i][j].x, negative_samples[i][j].y);
    }

    context.closePath();
    context.fill();
    context.stroke();
  }
});
$("#negatives").click(function (e) {
  e.preventDefault();
  if (poly_counter == 0) {
    if (lang == "en") alert("Please draw a polygon first.");
    else alert("Lütfen önce bir şekil çizin.");
    return;
  }
  if (negative_tag_counter == 0) {
    if (lang == "en") alert("Please select a negative tag first.");
    else alert("Lütfen önce negatif bir etiket seçin.");
    return;
  }
  negativeTagsRadios.forEach((radioButton) => {
    radioButton.checked = false;
  });
  coordinates.push({ label: label });
  negative_tag_counter = 0;
  negative_samples.push(coordinates);
  coordinates = [];
  context.clearRect(0, 0, cw, ch);

  context.lineWidth = 4;
  context.strokeStyle = "red";
  context.fillStyle = "rgba(255,0,0,.2)";
  for (var i = 0; i < negative_samples.length; i++) {
    context.beginPath();
    context.moveTo(negative_samples[i][0].x, negative_samples[i][0].y);
    for (var j = 1; j < negative_samples[i].length; j++) {
      context.lineTo(negative_samples[i][j].x, negative_samples[i][j].y);
    }

    context.closePath();
    context.fill();
    context.stroke();
  }
  context.strokeStyle = "green";
  context.fillStyle = "rgba(0,255,0,.2)";
  for (var i = 0; i < positive_samples.length; i++) {
    context.beginPath();
    context.moveTo(positive_samples[i][0].x, positive_samples[i][0].y);
    for (var j = 1; j < positive_samples[i].length; j++) {
      context.lineTo(positive_samples[i][j].x, positive_samples[i][j].y);
    }

    context.closePath();
    context.fill();
    context.stroke();
  }
  poly_counter = 0;
});
$("#clear").click(function (e) {
  e.preventDefault();
  if (poly_counter == 0) {
    if (lang == "en") alert("Please draw a polygon first.");
    else alert("Temizlemek için önce bir şekil çizmeniz gerekiyor.");
    return;
  }
  poly_counter = 0;
  coordinates = [];
  context.clearRect(0, 0, cw, ch);
});

$("#canvas").mousedown(function (e) {
  handleMouseDown(e);
});
function handleMouseDown(e) {
  // tell the browser we're handling this event
  e.preventDefault();
  e.stopPropagation();

  mouseX = parseInt(e.clientX - offsetX);
  mouseY = parseInt(e.clientY - offsetY);
  coordinates.push({ x: mouseX, y: mouseY });
  drawPolygon();
}

function drawPolygon() {
  // Aşağıdaki satır çizilirken çizimi bozuyor ama yeni bir şekle tıklandığında işler kolaylaşıyor.
  if (poly_counter != 0) {
    context.clearRect(0, 0, cw, ch);
  }
  poly_counter += 1;

  context.beginPath();
  context.moveTo(coordinates[0].x, coordinates[0].y);
  for (index = 1; index < coordinates.length; index++) {
    context.lineTo(coordinates[index].x, coordinates[index].y);
  }
  context.strokeStyle = "blue";
  context.closePath();
  context.stroke();
}
