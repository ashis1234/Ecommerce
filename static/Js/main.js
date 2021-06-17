var updatebtn = document.getElementsByClassName('update-cart')
// var quantitybtn = document.getElementsByClassName('chg-quantity')
// for(var i = 0; i < quantitybtn.length; ++i){
//     quantitybtn[i].addEventListener('click',function(){
//         var productid = this.dataset.product;
//         var action = this.dataset.action;
//         if(user === 'AnonymousUser'){
//             console.log('Not logged in');
//         }
//         else{
//             updateUserOrder(productid,action,1);
//         }
//     });
// }

for(var i = 0; i < updatebtn.length; ++i){
        updatebtn[i].addEventListener('click',function(){
        var productid = this.dataset.product;
        var action = this.dataset.action;
        if(user === 'AnonymousUser'){
            addCookieItem(productid,action)
        }
        else{
            updateUserOrder(productid,action,0);
        }
    });
}

function addCookieItem(productid,action){
    if(action == 'add'){
        if(cart[productid] == undefined){
            cart[productid] = {'quantity' : 1};
        }
        else
            cart[productid]['quantity'] += 1;
    }
    else{
        cart[productid]['quantity'] -= 1;
        if(cart[productid]['quantity'] <= 0){
            delete cart[productid]
        }
    }
    console.log(cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}


function updateUserOrder(productid,action,is_from_cart){
    var url = '/update_item/'
    fetch(url, {
        method : 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productid' : productid, 'action' : action,'is_from_cart':is_from_cart}),
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        location.reload();
    });
}