class Stack {
    constructor() {
        this.users = []
        this.passwords = []
    }

    push(username, password) {
        this.users.push(username)
        this.passwords.push(password)
    } 

} 
const pila = new Stack()

var dato1;
function Guardar() {
    const username = parseInt(document.getElementById('username').value);
     dato1 = pila.push(username);
    const password = parseInt(document.getElementById("password").value);
    var dato2 = pila.push(password);

    alert(dato2);

}

function forgot() {
    alert("Ni modo");
}
