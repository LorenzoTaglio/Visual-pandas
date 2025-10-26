document.addEventListener('DOMContentLoaded', function() {
    loadDataFrame();
});

// document.querySelector(".pandas").addEventListener("keydown", function(event){
//     if (event.target.classList.contains("cell") && event.key === "Enter"){
//         event.preventDefault();
//         updateCell(event.target);
//     }
// })
//     
// document.querySelector("#addCol").addEventListener("click", function(){
//     // Remove previous instances of momentary input
//     if (document.querySelector(".newInsert")){
//         document.querySelector(".dataframe thead th:has(.newInsert)").remove();
//     }
//     addColumn();
// })
// 
// document.querySelector("#addRow").addEventListener("click", async function(){
//     if (document.querySelector(".newInsert")){
//         document.querySelector(".dataframe thead th:has(.newInsert)").remove();
//     }
// 
//     if (await columnsLen() < 1){
//         console.log("No columns detected");
//         return;
//     }
//     await addRow();
// });

document.querySelector("#importDf").addEventListener("change", function(event){
    importDataFrame(event);
})

function importDataFrame(event){
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch("/import_dataframe", {
        method: "POST",
        body: formData
    })
    .then(response =>{
        if(!response.ok){
            return response.json().then(err => Promise.reject(err));
        }
        return response.json();  
    })
    .then(data => {
        if(data.success){
            // Create wrapper
            const newDf = document.createElement("div");
            newDf.id = data.df_id
            newDf.classList.add("pandas");

            // Add name
            const dfName = document.createElement("h2");
            dfName.innerText = data.name;
            newDf.appendChild(dfName);
            
            // Df table
            const dfTable = document.createElement("div");
            dfTable.classList.add("table");
            dfTable.innerHTML = data.html;
            newDf.appendChild(dfTable);

            // Add col btn
            const addColBtn = document.createElement("button");
            addColBtn.classList.add("addCol");
            addColBtn.innerText = "Add Column";
            newDf.appendChild(addColBtn);

            // Add row btn
            const addRowBtn = document.createElement("button");
            addRowBtn.classList.add("addRow");
            addRowBtn.innerText = "AddRow";
            newDf.appendChild(addRowBtn);
        

            document.body.appendChild(newDf);
        }
    })
}


async function columnsLen(){
    let columns = 0
    await fetch("/columns_len")
    .then(async response =>{
        if(!response.ok){
            return response.json().then(err => Promise.reject(err));
        }
        return response.json(); 
    })
    .then(async data =>{
        if (data.success){
            console.log("ENTERA!");
            columns = data.columnsLen;
        }
    })
    console.log(`Columns: ${columns}`)
    return columns;
}

function loadDataFrame(){
    fetch('/get_df')
    .then(response => response.json())
    .then(data =>{
        // document.querySelector(".pandas").innerHTML = data.html;
        console.log(data.html);
    })
    .catch(error=>{
        alert("Errore");
        console.error("Errore", error)
    })
}


function updateCell(cell){
    const cellId = cell.id;
    const [column, row] = cellId.split("_");
    fetch("/update_cell",{
        method: "POST",
        headers : {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            column: column,
            row: row,
            value: cell.value
        })
    }).then(response =>{
        if(!response.ok){
            return response.json().then(err => Promise.reject(err));
        }
        return response.json();  
    })
    .then(data => {
        if(data.success){
            document.querySelector(".pandas").innerHTML = data.html;
        }
    })
}

function addColumn(){
    const newTh = document.createElement("th")
    newTh.innerHTML = "<input type='text' id='insertColName' class='newInsert'>";
    document.querySelector(".dataframe thead tr").appendChild(newTh);
    document.querySelector("#insertColName").addEventListener("keydown", function(event){
        if (event.key !== "Enter"){
            return;
        }
        const columnName = this.value.trim();
        fetch("/add_column", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                column_name: columnName || undefined
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => Promise.reject(err));
            }
            return response.json();                  
        })
        .then(data => {
            if(data.success){
                document.querySelector(".pandas").innerHTML = data.html;
            }
        })
        .catch(error => {
            console.error('Errore:', error);
        });
    })
}


async function addRow(){
    fetch("/add_row")
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => Promise.reject(err));
        }
        return response.json();                  
    })
    .then(data => {
        if(data.success){
            document.querySelector(".pandas").innerHTML = data.html;
        }
    })
    .catch(error => {
        console.error('Errore:', error);
    });
}