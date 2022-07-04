// function func(){
//   return new Promise((resolve,reject)=>{
//       let error = false;
//       setTimeout(()=>{
//         if(!error)
//           resolve("Deleted");
//         else
//           reject("Failed to delete");
//       },5000)
//   })
// }


//working
// function fire(id){
//     Swal.fire({
//       title: 'Are you sure?',
//       text: "You won't be able to revert this!",
//       icon: 'warning',
//       showCancelButton: true,
//       confirmButtonColor: '#3085d6',
//       cancelButtonColor: '#d33',
//       confirmButtonText: 'Yes, delete it!',
//       showLoaderOnConfirm: true,
//       preConfirm: () => {
//         return fetch('/deleteticket/'+id)
//             .then(response => {
//                 console.log(response);
//                 if (!response.status) {
//                 throw new Error(response.statusText)
//                 }
//                 return response.json()
//             })
//             .catch(error => {
//                 Swal.showValidationMessage(
//                 `Request failed: ${error}`
//                 )
//             })
//       },
//       allowOutsideClick: () => !Swal.isLoading()
//     }).then((result) => {
//         console.log(result);
//       if (result.isConfirmed) {
//         Swal.fire(
//           'Deleted!',
//           'Your file has been deleted.',
//           'success'
//         )
//         .then(()=>{
//           location.reload();
//         })
        
//       }
//     })
//   }

//testing
function deleteTicket(id){
  Swal.fire({
    title: 'Are you sure?',
    text: "You won't be able to revert this!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, delete it!',
    showLoaderOnConfirm: true,
    allowOutsideClick: () => !Swal.isLoading(),
   
  }).then((result) => {
      console.log(result);
    if (result.isConfirmed) {
      var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
      $.ajax({
        method:'POST',
        url:'/deleteticket/',
        data : {id, 'csrfmiddlewaretoken':csrftoken},
        dataType:'json'
      }).done(function(data) {
          if(data.status){
            Swal.fire(
                'Deleted!',
                'Your file has been deleted.',
                'success'
              )
              .then(()=>{
                window.location.href = '/tickets';
              })
            
          }
          else{
            Swal.fire(
              'Failed!',
              'Your file has NOT been deleted.',
              'error'
            )
          }
      })
      .fail(function(data,error) {
        Swal.showValidationMessage(
          `Request failed: ${error}`
        )
      })
    }
  })
}

function changeStatus(id,status){
  Swal.fire({
    title: 'Are you sure?',
    text: "You won't be able to revert this!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, ' + ((status==1)?'Accept!':'Reject!'),
    showLoaderOnConfirm: true,
    allowOutsideClick: () => !Swal.isLoading(),
   
  }).then((result) => {

    if (result.isConfirmed) {
 
      var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

      console.log(status)
      $.ajax({
        method:'POST',
        url:'/changestatus/',
        data:{'id':id, 'status':status, 'csrfmiddlewaretoken':csrftoken}
      }).done(function(data) {
          console.log(data)
          if(data.status){
            Swal.fire(
              status==1?'Accepted!':'Rejected!',
                'Your file has been ' + (status==1?'accepted.':'rejected.'),
                'success'
              )
              .then(()=>{
                location.reload();
              })
            
          }
          else{
            Swal.fire(
              'Failed!',
              'Your file has NOT been '+ (status==1?'accepted.':'rejected.'),
              'error'
            )
          }
      })
      .fail(function(xhr, status, error) {
        Swal.showValidationMessage(
          `Request failed: ${error}`
        )
      })
    }
  })
}




// function fire(){
//     Swal.fire({
//       title: 'Are you sure?',
//       text: "You won't be able to revert this!",
//       icon: 'warning',
//       showCancelButton: true,
//       confirmButtonColor: '#3085d6',
//       cancelButtonColor: '#d33',
//       confirmButtonText: 'Yes, delete it!',
//       showLoaderOnConfirm: true,
//       preConfirm: () => {
//         return func()
//             .then(response => {
//             // if (!response.ok) {
//             //   throw new Error(response.statusText)
//             // }
//             return response
//           })
//           .catch(error => {
//             Swal.showValidationMessage(
//               `Request failed: ${error}`
//             )
//           })
//       },
//       allowOutsideClick: () => !Swal.isLoading()
//     }).then((result) => {
//       if (result.isConfirmed) {
//         Swal.fire(
//           'Deleted!',
//           'Your file has been deleted.',
//           'success'
//         )
//       }
//     })
//   }