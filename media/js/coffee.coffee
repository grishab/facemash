class Loader
  constructor: ->

  apply: ->
      $.getJSON('/chose', @renderChose)

  renderChose: (data) =>
      parent = $('#photo_chose')
      parent.empty()
      for user in data
          li = $('<li></li>')
          div = $('<div></div>')
          img = $('<img width="247" src="'+user.photo_big+'" />')
          li.append(div.append(img))
          li.data('uid',user.uid)
          li.click((event)=> @choseUser(event))
          parent.append(li)
          console.log(user.uid)

  choseUser: (event) ->
      uid = $(event.currentTarget).data('uid')
      $.get('/chose/'+uid)
      @apply()

window.loader = new Loader()

$(document).ready(->
    loader.apply()
)
