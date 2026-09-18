
const btn =document.getElementById("signup")

btn.addEventListener("click",function(){
   let pic=document.getElementById("file").files[0]
   let email=document.getElementById("email").value
   let password=document.getElementById("password").value
   let birth=document.getElementById("birth").value
    let formdata=new FormData()
    let xhr=new XMLHttpRequest()
    xhr.open("POST","http://localhost:8001/signup",false)
    xhr.withCredentials=true
    formdata.append("pic",pic)
    formdata.append("email",email)
    formdata.append("password",password)
    formdata.append("birth",birth)
alert("before send")    
    xhr.send(formdata)
    alert("send")
   let response=xhr.response
   response=JSON.parse(response)
    if(xhr.status==200){
      
        window.location.href="otp.html?userid="+response

    }
})




