document.addEventListener("DOMContentLoaded", function () {
    let cartCountElement = document.getElementById('cart-count'); // Make sure this exists in HTML
    if (cartCountElement) {
        cartCountElement.textContent = "0"; // ✅ Only modify if element exists
    } else {
        console.error("Element with ID 'cart-count' not found.");
    }
});


const container=document.querySelector('.co');
const LoginLink=document.querySelector('.SignInlink')
const Logout=document.querySelector('.logout')
const RegisterLink=document.querySelector('.SignUplink')
const Login_Load=document.querySelector('.Login-Load')
const Cancle=document.querySelector('.Cancle')
const Submit=document.querySelector('.submit')
const Cancle2=document.querySelector('.cancle2')


Logout.addEventListener('click',()=>{
    container.classList.remove('new');


    })
    
LoginLink.addEventListener('click',()=>{
container.classList.remove('active');
})

Login_Load.addEventListener('click',()=>{
container.classList.add('activeee');
})
Cancle.addEventListener('click',()=>{
container.classList.remove('activeee');
})


RegisterLink.addEventListener('click',()=>{
container.classList.add('active');
})

  
Cancle2.addEventListener('click',()=>{
    container.classList.remove('activeee'); })


    function cancle() {
        container.classList.remove('activeee');
   }
   
   function mayur() {container.classList.add('activeee');

   }

   function mayur1() {
    container.classList.add('active');

   }
   
   
   function mayur2() {
    container.classList.remove('active');

   }
   
   function toggleProfile() {container.classList.add('activeee');
    container.classList.add('new');
    

    const header=document.querySelector('.hed');

    header.classList.add('my');
    header.classList.add('my'); 
   }


    function addToCart(productId) {
        fetch('/add_to_cart', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => console.error('Error:', error));
    }
