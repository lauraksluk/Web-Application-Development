"use strict"


function loadPosts() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }
    xhr.open("GET", "socialnetwork/get-global", true)
    xhr.send()
}

function loadPostsFollower() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }
    xhr.open("GET", "socialnetwork/get-follower", true)
    xhr.send()
}

function add_comment(postObj) {
    let commentId = "id_comment_input_text_" + String(postObj.id)
    let commentTextElement = document.getElementById(commentId)
    let commentTextValue = commentTextElement.value 

    commentTextElement.value = ''
    displayError('')

    let xhr = new XMLHttpRequest()
    updatePage(xhr)
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }
    let pathStr = addCommentURL(myUserId)
    xhr.open("POST", pathStr, true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhr.send("comment_text="+commentTextValue+"&post_id="+postObj.id+"&csrfmiddlewaretoken="+getCSRFToken())
    updatePage(xhr)
    updatePage(xhr)
    updatePage(xhr)
}

function updatePage(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updatePostList(response)
        return
    }
    if (xhr.status == 0) {
        //displayError("Cannot connect to server")
        return
    }
    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function updatePostList(postCommentDict) {
    let postList = postCommentDict['posts']
    let commentList = postCommentDict['comments']

    let list = document.getElementById("my-posts-go-here")
    let listAllPosts = list.children
    var listOfAllPostIds = []
    var dictAllCommentIds = {}

    if (listAllPosts.length > 0) {
        for (let i = 0; i < listAllPosts.length; i++) {
            let item = listAllPosts[i]
            let idStr = item.children[0].children[0].children[0].children[0].children[0].id
            let n = parseInt(idStr.slice(12, idStr.length))
            listOfAllPostIds.push(n)
            dictAllCommentIds[n] = []
            let comms = item.children[1].children[0].rows
            if (comms.length > 1) {
                for (let m = 0; m < comms.length - 1; m++) {
                    let idCommentStr = comms[m].cells[0].children[0].id

                    let nC = parseInt(idCommentStr.slice(15, idCommentStr.length))
                    dictAllCommentIds[n].push(nC)
                }
            }
            
        }
    }

    let begin = list
    for (let j = 0; j < postList.length; j++) {
        let indivPost = postList[j]
        if (!listOfAllPostIds.includes(indivPost.id)) {
            if (list.childElementCount == 0) {
                begin = list
            } else {
                begin = list.firstElementChild
            }
            let outerPostDiv = addOuterPostDiv(list, begin, indivPost)
            let postDiv = addPostProfileLink(outerPostDiv, indivPost)
            postDiv = addPostText(postDiv, indivPost)
            let commentDiv = addCommentDiv(outerPostDiv, indivPost)
        }
    }

    for (let k = 0; k < commentList.length; k++) {
        let indivComment = commentList[k]
        let commentPostId = indivComment.post
        let commentId = indivComment.id
        let valueListCommentIds = dictAllCommentIds[commentPostId]

        if (!valueListCommentIds || valueListCommentIds.length == 0 || !valueListCommentIds.includes(commentId)) {
            let commentDivId = "my-comments-go-here-for-post-" + String(commentPostId)
            let tablePtr = document.getElementById(commentDivId).children[0] //table
            addCommentHTML(tablePtr, indivComment)
        }
    }
}

function addCommentHTML(table, comment) {
    let tbody = table.firstElementChild
    let row = document.createElement("tr")
    let col = document.createElement("td")
    col.className = "eachcomment"
    row.appendChild(col)
    tbody.appendChild(row)

    let commentDiv = document.createElement("div")
    commentDiv.id = "id_comment_div_" + String(comment.id)
    commentDiv.className = "eachcomment"
    let commentBy = document.createTextNode("Comment by ")
    commentDiv.appendChild(commentBy)    

    let commentProfile = document.createElement("a")
    let urlStr = otherProfileURL(comment.userid)
    commentProfile.setAttribute("href", urlStr)
    commentProfile.id = "id_comment_profile_" + String(comment.id)
    commentProfile.innerHTML = comment.first_name + " " + comment.last_name + " "
    commentDiv.appendChild(commentProfile)

    let commentText = document.createElement("span")
    commentText.id = "id_comment_text_" + String(comment.id)
    commentText.textContent = comment.text + " "
    commentDiv.appendChild(commentText)

    let commentDate = document.createElement("span")
    commentDate.id = "id_comment_date_time_" + String(comment.id)
    commentDate.style = "font-style:italic;"
    let date = new Date(comment.creation_time)
    let time = date.toLocaleTimeString()
    let dateStr = date.toLocaleDateString() + " " + time.slice(0, time.length-6) + " " + time.slice(time.length-2, time.length)
    commentDate.textContent = dateStr
    commentDiv.appendChild(commentDate)

    col.appendChild(commentDiv)
}

function addCommentDiv(outerPostDiv, postObj) {
    let commentDiv = document.createElement("div")
    commentDiv.id = "my-comments-go-here-for-post-" + String(postObj.id)
    outerPostDiv.appendChild(commentDiv)
    
    let commentTable = document.createElement("table")
    commentTable.className = "comment12"
    let tbody = document.createElement("tbody")
    let foot = document.createElement("tfoot")
    commentTable.appendChild(tbody)
    commentTable.appendChild(foot)
    commentDiv.appendChild(commentTable)

    let row = document.createElement("tr")
    let col = document.createElement("td")
    col.className = "newcommentbox"
    row.appendChild(col)
    foot.appendChild(row)

    let label = document.createElement("label")
    label.htmlFor = "id_comment_input_text_" + String(postObj.id)
    label.innerHTML = "Comment: "
    col.appendChild(label)

    let input = document.createElement("input")
    input.type = "text"
    input.name = "new"
    input.id = "id_comment_input_text_" + String(postObj.id)
    col.appendChild(input)

    let submit = document.createElement("button")
    submit.type = "submit"
    submit.id = "id_comment_button_" + String(postObj.id)
    submit.className = "submit"
    submit.innerHTML = "submit"
    submit.onclick = function() {
        add_comment(postObj);
    }
    col.appendChild(submit)
    
    return commentTable
}

function addPostText(postDiv, postObj) {
    let postBy = document.createTextNode("Post by ")
    postDiv.appendChild(postBy)

    let postLink = document.createElement("a")
    let urlStr = otherProfileURL(postObj.userid)
    postLink.setAttribute("href", urlStr)
    postLink.id = "id_post_profile_" + String(postObj.id)
    postLink.innerHTML = postObj.first_name + " " + postObj.last_name + " "
    postDiv.appendChild(postLink)

    let postText = document.createElement("span")
    postText.id = "id_post_text_" + String(postObj.id)
    postText.textContent = postObj.text + " "
    postDiv.appendChild(postText)

    let postTime = document.createElement("span")
    postTime.id = "id_post_date_time_" + String(postObj.id)
    postTime.style = "font-style:italic;"
    let date = new Date(postObj.time)
    let time = date.toLocaleTimeString()
    let dateStr = date.toLocaleDateString() + " " + time.slice(0, time.length-6) + " " + time.slice(time.length-2, time.length)
    postTime.textContent = dateStr
    postDiv.appendChild(postTime)
    return postDiv
}

function addOuterPostDiv(head, firstNode, postObj) {
    let first = document.createElement("div")
    first.id = "fullpost" + String(postObj.id)
    first.className = "fullpost1"
    if (head.childElementCount == 0) {
        head.appendChild(first)
    } else {
        head.insertBefore(first, firstNode)
    }
    return first
}

function addPostProfileLink(first, postObj) {
    let table = document.createElement("table")
    table.id = "post" + String(postObj.id)
    table.className = "post1"
    let thead = document.createElement("thead")
    let tbody = document.createElement("tbody")
    table.appendChild(thead)
    table.appendChild(tbody)
    first.appendChild(table)
    let row = document.createElement("tr")
    let col = document.createElement("th")
    row.appendChild(col)
    thead.appendChild(row)
    let postDiv = document.createElement("div")
    postDiv.id = "id_post_div_" + postObj.id
    postDiv.className = "post1"
    col.appendChild(postDiv)
    return postDiv
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    if (message) {
        errorElement.innerHTML = message
    }
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}