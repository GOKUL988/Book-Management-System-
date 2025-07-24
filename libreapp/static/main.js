function toggleSidebar() {
    const sidebar = document.getElementById("mySidebar");
    const body = document.getElementById("maintoggle"); 

    if (sidebar.style.width === "250px") {
        sidebar.style.width = "0";
        //body.style.width = "100%"
    } else {
        sidebar.style.width = "250px";
        //body.style.width = "80%"
    }
}
function cancel(){
    pop = document.getElementById("message_pop"); 
    pop.remove()
}
setTimeout(() => {
    const pop = document.getElementById("message_pop"); 
    if (pop) pop.remove(); 
}, 2000);

function Addmore(){
    let table= document.getElementById("Stock");
    let newField = `
        <tr>

            <td><input type="text" name="booktitle[]" required></td>
            <td><input type="text" name="authorname[]" required></td>
            <td><input type="text" name="edition[]" required></td>
            <td><input type="text" name="yearofpub[]" required></td>
            <td><input type="text" name="qun[]"  required></td>
            <td><input type="text" name="rate[]" required></td>
            <td>
                <input list="sub1" name="categ[]" type="text"  id="cateo" required> 
                <datalist id="sub1">
                    {% for i in sub1%} 
                    <option value="{{i.cate1}}"></option>
                    {% endfor %}
                </datalist>
            </td>
            <td>
                <input list="sub1" name="classfic[]" type="text" required>
                <datalist id="sub1">
                    {%for i in sub1%} 
                    <option value="{{i.sub}} - {{i.cate1}}"></option>
                    {%endfor%}
                </datalist>
            </td>
            <td>
                <input list="rac" type="text" name="rack[]" required>
                <datalist id="rac">
                    {%for i in rac %} 
                    <option value="{{i.rack_sh}}"></option>
                    {% endfor%}
                </datalist>
            </td>
        </tr>
    `;
    table.insertAdjacentHTML('beforeend' , newField);
}

function calc(el){
    const row = el.closest("tr");
    const rate = parseFloat(row.querySelector(".rate").value) || 0;
    const qty = parseFloat(row.querySelector(".qty").value) || 0;
    const amount =rate * qty;
    row.querySelector(".amount").value = amount.toFixed(2);
}
window.onload = function() {
    document.querySelectorAll("tr").forEach(row =>{
        const rte = row.querySelector(".rate");
        if (rte){
            calc(rte);
        }
    });
};
function prt(){
    if (window.print){
         document.getElementById("hide").style.display='None';
         window.print();

         setTimeout(() =>{
            document.getElementById("hide").style.display='inline';
            document.getElementById("hide").style.width='90%';
         },100);
    }
}
function printInvoice() {
    document.getElementById('back').style.display = "none";
    document.getElementById('remove').style.display = "none";

    setTimeout(function () {
        window.print();
        document.getElementById('back').style.display = "inline";
        document.getElementById('remove').style.display = "inline";
    }, 300);
}

    function more(){
        let table = document.getElementById("Moretab");
        let newField= `
        <tr>
             <td colspan="2">
            <input list="sto_lst" type="text" name="isbn_dt[]" oninput="fillRate(this)" class="booktitle" required>
                <datalist id="sto_lst">
                    {% for i in sto_lst %}
                    <option value="{{ i.isbn }}" data-isbn="{{ i.isbn }}" data-rate="{{ i.rate }}" data-book="{{i.booktitle}}">{{i.isbn}} - {{i.booktitle}}</option>
                    {% endfor %}
                </datalist>
        </td>
        <td><input type="text" name="book_dt[]" class="book" required> </td>
        <td><input type="number" name="perunt[]" class="rate" oninput="calculateAmount(this)" required></td>
        <td><input type="number" name="qunt[]" class="qty" oninput="calculateAmount(this)" required></td>
        <td><input type="text" name="amount[]" class="amount" readonly></td>
        </tr>
        `;
        table.insertAdjacentHTML('beforeend', newField);
    }

function calculateAmount(el) {
    const row = el.closest("tr");
    const rate = parseFloat(row.querySelector(".rate").value) || 0;
    const qty = parseFloat(row.querySelector(".qty").value) || 0;
    const amount = rate * qty;
    row.querySelector(".amount").value = amount.toFixed(2);

    let total = 0;
    document.querySelectorAll(".amount").forEach(a => {
        total += parseFloat(a.value) || 0;
    });
    document.getElementById("total").innerText = total.toFixed(2);
     document.getElementById("to_mn").value = total.toFixed(2);
}

function fillRate(input) {
    const value = input.value;
    const rateInput = input.closest("tr").querySelector(".rate");
    const bookInput = input.closest("tr").querySelector(".book");

    const options = document.querySelectorAll("#sto_lst option");

    for (let option of options) {
        if (option.value === value) {
            bookInput.value = option.getAttribute("data-book");
            rateInput.value = option.getAttribute("data-rate");
            break;
        }
    }
}

