const btn=document.getElementById("Login")

btn.addEventListener("click",function(){
 let email=document.getElementById("email").value
let password=document.getElementById("password").value
 let xhr=new XMLHttpRequest()
 xhr.open("POST","http://localhost:8001/login",false)
 xhr.withCredentials=true
 xhr.setRequestHeader("Content-Type","application/json")
 
 xhr.send(JSON.stringify({
    email:email,
    password:password
 }))

 if(xhr.status==200){
   alert("correct login")
   window.location.assign("facebook_dashboard.html")

 }
 else{
   alert("invalid status:"+xhr.status)
 }
})