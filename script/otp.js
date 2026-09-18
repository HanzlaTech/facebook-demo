
let params = new URLSearchParams(window.location.search);

let userid = params.get("userid");
const otp_btn=document.getElementById("otp")

otp_btn.addEventListener("click",function(){
    let otp=document.getElementById("otp_value").value
    let xhr=new XMLHttpRequest()
    alert("h")
    xhr.open("POST","http://localhost:8001/otp",false)
    xhr.withCredentials=true
    xhr.setRequestHeader("Content-type","application/json")

    xhr.send(JSON.stringify({
        "otp":otp,
        "userid":userid
    }))
    if(xhr.status==200){
        alert("valid otp")
        window.location.assign("facebook_dashboard.html")
    }
   else{
    alert("invalid otp, Recheck the otp again")
    
   }
})