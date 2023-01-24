function delBlog(blog_id){
    var id = blog_id.split('-')[1]
    console.log(id)
    var confirmation = document.getElementById('confirmationMessage')
    confirmation.innerHTML = 'Are you sure you want to DELETE this blog?'
    toggleConfirmation()
    $("#userConfirmed").on('click',function(){
        $.ajax({
            url: "/user/delete-blog/"+id,
            success : function(json) {
                closeConfirmationBox()
                $( ".blogList" ).load(" .blogList" );
            }
        })
    });
  }
  function toggleConfirmation(){
    $('#popupModal').addClass('toggle-confirmation');
  }
  function closeConfirmationBox(){
    $('#popupModal').removeClass('toggle-confirmation');
  }