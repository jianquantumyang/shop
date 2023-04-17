const search = document.querySelector('.search');
const search_go = document.querySelector('.search_go');
search_go.addEventListener('click',()=>{

    if(search.value==""){
        alert("Введите слова в запрос");
        
    
    }
    else{
        window.location = `/search?name=${search.value}`;
    }
})