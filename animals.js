const API = "http://localhost:8000";

function addAnimal(list, animal) {
  const item = document.createElement("li");
  item.className = "animal-row";

  if (animal.image) {
    const image = document.createElement("img");
    image.src = animal.image;
    image.alt = animal.name;
    item.appendChild(image);
  }

  const info = document.createElement("div");
  info.className = "animal-info";

  const name = document.createElement("h2");
  name.textContent = animal.name;

  const meta = document.createElement("p");
  meta.className = "animal-meta";
  meta.textContent = animal.species + " · " + animal.breed + " · " + animal.gender + " · " + animal.age;

  const status = document.createElement("p");
  status.className = "animal-status";
  if (animal.status === "Available") {
    status.classList.add("is-available");
  }
  status.textContent = animal.status;

  const edit = document.createElement("a")
  edit.className = "edit-button";
  edit.textContent = "Edit";
  edit.href = "#animal-form";
  edit.addEventListener("click", () => {
    editingId = animal.id;
    editingImage = animal.image || "";
    document.querySelector("#animal-form [name=name]").value = animal.name;
    document.querySelector("#animal-form [name=species]").value = animal.species;
    document.querySelector("#animal-form [name=breed]").value = animal.breed;
    document.querySelector("#animal-form [name=gender]").value = animal.gender;
    document.querySelector("#animal-form [name=age]").value = animal.age;
    document.querySelector("#animal-form [name=description]").value = animal.description;
    document.querySelector("#animal-form [name=status]").value = animal.status;
  });
  

  const remove = document.createElement("button");
  remove.className = "delete-button";
  remove.textContent = "Delete";
  remove.addEventListener("click", () => {
    const yes = confirm("Delete " + animal.name + "?");
    if (yes) {
      fetch(API + "/animals/" + animal.id, { method: "DELETE" })
        .then(() => item.remove());
    }
  })

  info.append(name, meta, status);                
  if (animal.description) {
    const description = document.createElement("p");
    description.className = "animal-description";
    description.textContent = animal.description;
    info.appendChild(description);
  }

  item.appendChild(info);
  list.appendChild(item);
  info.appendChild(edit);
  info.appendChild(remove)

}

fetch(API + "/animals")
  .then((response) => response.json())
  .then((animals) => {
    const list = document.querySelector("#animal-list");
    animals.forEach((animal) => addAnimal(list, animal));
  }); 


  let queuedImagesArray = [],
  editingId = null,                                     // editingId = null => Adding; when edit is not null => Editing
  editingImage = "",
  queuedDiv = document.querySelector(".queued-form"),
  inputDiv = document.querySelector(".input-div"),
  input = document.querySelector(".input-div input");

  // QUEUE IN FRONTEND IMAGES
  input.addEventListener("change", () => {
    const files = input.files
    for (let i =0; i < files.length; i++){
      queuedImagesArray.push(files[i])
    }
    input.value = ""
    displayQueuedImages()
  })

  inputDiv.addEventListener("drop", (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    for(let i=0; i < files.length; i++){
      if (!files[i].type.match("image")) continue
      if(queuedImagesArray.every(image => image.name !== files[i].name))
        queuedImagesArray.push(files[i])
    }
    displayQueuedImages()
  })


function displayQueuedImages(){
  let images = ""
  queuedImagesArray.forEach((image, index) => {
    images += `<div class="image">
                <img src="${URL.createObjectURL(image)}" alt="image">
                <span onclick="deleteQueuedImage(${index})">&times;</span>
              </div>`
  })
  queuedDiv.innerHTML= images;
}

function deleteQueuedImage(index){
  queuedImagesArray.splice(index, 1)
  displayQueuedImages()
}

function addNewAnimal(e) {
  e.preventDefault();

  const sendAnimal = (imagePath) => {
    const animal = {
      name: document.querySelector("#animal-form [name=name]").value,
      species: document.querySelector("#animal-form [name=species]").value,
      breed: document.querySelector("#animal-form [name=breed]").value,
      gender: document.querySelector("#animal-form [name=gender]").value,
      age: document.querySelector("#animal-form [name=age]").value,
      description: document.querySelector("#animal-form [name=description]").value,
      status: document.querySelector("#animal-form [name=status]").value,
      image: imagePath,
    };

    const url = editingId ? API + "/animals/" + editingId : API + "/animals";
    const method = editingId ? "PUT" : "POST";

    fetch(url, {
      method: method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(animal),
    })
      .then((response) => response.json())
      .then(() => {
      editingId = null;
      editingImage = "";
      queuedImagesArray = [];
      displayQueuedImages();
      document.querySelector("#animal-form").reset();
      return fetch(API + "/animals");
    })
    .then((response) => response.json())
    .then((animals) => {
      const list = document.querySelector("#animal-list");
      list.replaceChildren();
      animals.forEach((animal) => addAnimal(list, animal));
    });
  };

  if (queuedImagesArray.length === 0) {
    sendAnimal(editingImage);
    return;
  }

  const formData = new FormData();
  queuedImagesArray.forEach((image, index) => {
    formData.append("file[" + index + "]", image);
  });

  fetch(API + "/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      sendAnimal((data.saved || [])[0] || "");
    });
}
document.querySelector("#animal-form").addEventListener("submit", addNewAnimal);
document.querySelector(".add-button").addEventListener("click", () => {
  editingId = null;
  editingImage = "";
  queuedImagesArray = [];
  displayQueuedImages();
  document.querySelector("#animal-form").reset();
});