$(document).ready(->
  console.log('heare')
  $.getJSON('/chose', (data)-> 
    console.log('dsad')
    console.log('before i get full data',data)
    $('body').append('<img src="'+data['photo']+'">')
  )
  console.log('fine working')
)
