const container = document.getElementById('predicted');
const output = document.getElementById('output');

const STRING = 'restlessness,lethargy,patches_in_throat,irregular_sugar_level,cough,high_fever,sunken_eyes,breathlessness,sweating,dehydration,indigestion,headache,yellowish_skin,dark_urine,nausea,loss_of_appetite,pain_behind_the_eyes,back_pain,constipation,abdominal_pain';
const arrayOfWords = STRING.split(',');

console.log(arrayOfWords, arrayOfWords.length);

const updatedWords = arrayOfWords.map(item => {
    const arrayOFSplittedWords = item.split('_');
    return arrayOFSplittedWords.join(' ');
})

function updateDOM(WordsArray){
    var i = 0;     
        
    while(i < WordsArray.length){
        if (WordsArray[i] !== '') {
            var div = document.createElement('div');
            div.setAttribute('class', 'form-group')

            var chk = document.createElement('input'); 
            chk.setAttribute('type', 'checkbox');      
            chk.setAttribute('id', 'prediction-' + i);
            chk.setAttribute('value', i+1);
            chk.setAttribute('name', 'Predictions');
            chk.setAttribute('class', 'form-control col-md-12');
            container.appendChild(chk);

            var lbl = document.createElement('label'); 
            lbl.setAttribute('for', 'prediction-' + i);
        
            lbl.appendChild(document.createTextNode(WordsArray[i]));

            container.appendChild(lbl);
        
            i++;
        }
    }
}

updateDOM(updatedWords);

const CheckedArray = new Array();

const submit = document.getElementById('submit').addEventListener('click', ()=> {
     $("input:checkbox[name=Predictions]:checked").each(function(){
        CheckedArray.push(Number($(this).val()));
    });

    const finalArray = new Array(20).fill(0);
    for(var i=0; i< CheckedArray.length; i++){
        finalArray[CheckedArray[i]-1]=1;
    }

    const stringVal = JSON.stringify(finalArray.join(''))
    console.log(stringVal)

    $.get("http://127.0.0.1:5000/prediction/"+stringVal, function (data) {
            console.log(data)
            localStorage.setItem("pred", data);
            output.innerHTML = data;
        })
        
})

