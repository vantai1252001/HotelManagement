function addToBooking(id, name, price) {
    event.preventDefault()

    fetch('/api/add-booking', {
        method: 'post',
        body: JSON.stringify( {
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res){
        return res.json()
    }).then(function(data){
        console.info(data)
        let counter = document.getElementsByClassName('booking-counter')
        for (let i = 0; i<counter.length; i++)
            counter[i].innerText = data.total_quantity
    }).catch(function(err){
        console.error(err)
    })
}


function pay(){
    if (confirm('Bạn chắc chắn muốn thanh toán không ?')==true){
        fetch('/api/pay', {
                method: 'post'
            }).then(res => res.json()).then(data => {
                if (data.code == 200)
                    alert('Thanh toán thành công!')
                    location.reload()
            }).catch(err => console.error(err))
    }
    else
        alert('Thanh toan that bai')
}


function updateBooking(id, obj){
    fetch('/api/update-booking', {
        method: 'put',
        body:JSON.stringify({
            'id': id,
            'quantity': parseInt(obj.value)
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let counter = document.getElementsByClassName('booking-counter')
        for (let i = 0; i < counter.length; i++)
            counter[i].innerText = data.total_quantity

        let amount = document.getElementById('total-amount')
        amount.innerText = new Intl.NumberFormat().format(data.total_amount)
    })
}



function deleteBooking(id){
    if(confirm("Bạn chắc chắn xóa phòng này không? ") == true){
        fetch('/api/delete-cart/' + id, {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            let counter = document.getElementsByClassName('booking-counter')
            for (let i = 0; i < counter.length; i++)
                counter[i].innerText = data.total_quantity

            let amount = document.getElementById('total-amount')
            amount.innerText = new Intl.NumberFormat().format(data.total_amount)

            let e = document.getElementById("room" + id)
            e.style.display = 'none'
        }).catch(err => console.error(err))
    }
}