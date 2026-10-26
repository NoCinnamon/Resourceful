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
  if (animal.status === "Adopted") {
    status.classList.add("is-adopted");
  }
  status.textContent = animal.status;

  const edit = document.createElement("a")
  edit.className = "edit-button";
  edit.textContent = "Edit";
  edit.href = "#animal-form";

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

fetch ( API + "/animals")                       // ajax
  .then((response) => response.json())
  .then((animals) => {
    const list = document.querySelector("#animal-list");
    animals.forEach((animal) => addAnimal(list, animal));
  });