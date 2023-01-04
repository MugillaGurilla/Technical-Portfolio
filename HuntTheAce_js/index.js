const cardObjectDefinitions = 
[
    {id:1, imagePath: '/Assets/card-KingHearts.png'},
    {id:2, imagePath: '/Assets/card-JackClubs.png'},
    {id:3, imagePath: '/Assets/card-QueenDiamonds.png'},
    {id:4, imagePath: '/Assets/card-AceSpades.png'},
]

const aceId = 4
const cardBackImgPath = '/Assets/card-back-Blue.png'
const cardContainerElem = document.querySelector('.card-container')
const playGameButtonElem = document.getElementById('playGame')
const collapsedGridAreaTemplate = '"a a" "a a"'
const cardCollectionCellClass = '.card-pos-a'
const numCards = cardObjectDefinitions.length

let cardPositions = []
let cards = []
let gameInProgress = false
let shufflingInProgress = false
let cardsRevealed = false
let roundNum = 0
let maxRounds = 4
let score = 0
let gameObj = {}

const localStorageGameKey = "HTA" 
const currentGameStateElem = document.querySelector('.current-status')
const scoreContainerElem = document.querySelector('.header-score-container')
const scoreElem = document.querySelector('.score')
const roundContainerElem = document.querySelector('.header-round-container')
const roundElem = document.querySelector('.round')

const winColour = 'green'
const loseColour = 'red'
const primaryColour = 'black'

loadGame()

function endRound()
{
    setTimeout(() =>
    {
        if(roundNum == maxRounds)
        {
            gameOver()
            return
        }
        else 
        {
            startRound()
        }
    }, 3000)
}

function gameOver()
{
    updateStatusElement(scoreContainerElem, "none")
    updateStatusElement(roundContainerElem, "none")
    const gameOverMessage = `Game Over! Final score - <span class='badge'>${score}</span>.
                            Click 'Play game' button to play again!`
    updateStatusElement(currentGameStateElem, "block", primaryColour, gameOverMessage)
    gameInProgress = false
    playGameButtonElem.disabled = false
}

function chooseCard(card) 
{
    if(canChooseCard()) 
    {
        evaluateCardChoice(card)
        saveGameObjectToLocalStorage(score, roundNum)
        flipCard(card, false)

        setTimeout(() =>
        {
            flipCards(false)
            updateStatusElement(currentGameStateElem, "block", primaryColour, "Card positions revealed....")
            endRound()
        }, 3000)
        cardsRevealed = true
    }
}

function calculateScoreToAdd(roundNum) 
{
    if(roundNum == 1)
    {
        return 100
    }
    else if(roundNum == 2)
    {
        return 50
    }
    else if(roundNum == 3)
    {
        return 25
    }
    else 
    {
        return 10
    }
}

function calculateScore()
{
    const scoreToAdd = calculateScoreToAdd(roundNum)
    score = score + scoreToAdd
}

function updateScore()
{
    calculateScore()
    updateStatusElement(scoreElem, "block", primaryColour, `<span class='badge'>${score}</span>`)
}

function updateStatusElement(elem, display, colour, innerHTML)
{
    elem.style.display = display 

    if(arguments.length > 2)
    {
        elem.style.color = colour
        elem.innerHTML = innerHTML
    }
}

function outputChoiceFeedback(hit)
{
    if(hit)
    {
        updateStatusElement(currentGameStateElem, "block", winColour, "Hit!!! - Well Done!! :)")
    }
    else
    {
        updateStatusElement(currentGameStateElem, "block", loseColour, "Missed!!! :(")
    }
}

function evaluateCardChoice(card)
{
    if(card.id == aceId)
    {
        updateScore()
        outputChoiceFeedback(true)
    }
    else
    {
        outputChoiceFeedback(false)
    }
}

function canChooseCard()
{
    return gameInProgress == true && !shufflingInProgress && !cardsRevealed
}

function loadGame()
{
    createCards()
    cards = document.querySelectorAll('.card')
    cardFlyInEffect()
    playGameButtonElem.addEventListener('click', ()=>startGame())
}

function checkForIncompleteGame() 
{
    const serialisedGameObj = getLocalStorageItemValue(localStorageGameKey)
    if (serialisedGameObj)
    {
        gameObj = getObjectFromJSON(serialisedGameObj)

        if (gameObj.round >= maxRounds)
        {
            removeLocalStorageItem(localStorageGameKey)
        }
        else 
        {
            if (confirm('Would you like to continue with your last game?'))
            {
                score = gameObj.score
                roundNum = gameObj.round
            }
        }
    }
}

function startGame()
{
    initialiseNewGame()
    startRound()
}

function initialiseNewGame()
{
    score = 0 
    roundNum = 0

    checkForIncompleteGame()

    shufflingInProgress = false

    updateStatusElement(scoreContainerElem, "flex")
    updateStatusElement(roundContainerElem, "flex")
    updateStatusElement(scoreElem, "block", primaryColour, `Score <span class='badge'>${score}</span>`)
    updateStatusElement(roundElem, "block", primaryColour, `Round <span class='badge'>${roundNum}</span>`)

}

function startRound()
{
    initialiseNewRound()
    collectCards()
    flipCards(true)
    shuffleCards()
}

function initialiseNewRound()
{
    roundNum++
    playGameButtonElem.disabled = true
    gameInProgress = true
    shufflingInProgress = true
    cardsRevealed = false

    updateStatusElement(currentGameStateElem, "block", primaryColour, "Shuffling...")
    updateStatusElement(roundElem, "block", primaryColour, `Round <span class='badge'>${roundNum}</span>`)

}

function collectCards()
{
    transformGridArea(collapsedGridAreaTemplate)
    addCardsToGridAreaCell(cardCollectionCellClass)
}

function transformGridArea(areas)
{
    cardContainerElem.style.gridTemplateAreas = areas
}

function addCardsToGridAreaCell(cellPositionClassName)
{
    const cellPositionElem = document.querySelector(cellPositionClassName)

    cards.forEach((card, index) => 
    {
        addChildElement(cellPositionElem, card)
    })
}

function flipCard(card, flipToBack)
{
    const innerCardElem = card.firstChild
    
    if (flipToBack && !innerCardElem.classList.contains('flip-it'))
    {
        innerCardElem.classList.add('flip-it')
    }
    else if (innerCardElem.classList.contains('flip-it'))
    {
        innerCardElem.classList.remove('flip-it')
    }
}

function flipCards(flipToBack)
{
    cards.forEach((card, index) => 
    {
        setTimeout(() =>
        {
            flipCard(card, flipToBack)
        }, index * 100)
    })
}

function cardFlyInEffect()
{
    const id = setInterval(flyIn, 5)
    let cardCount = 0
    let count = 0

    function flyIn()
    {
        count++
        if (cardCount == numCards)
        {
            clearInterval(id)
            playGameButtonElem.style.display = "inline-block"
        }
        if (count == 1 || count == 250 || count == 500 || count == 750)
        {
            cardCount++
            let card = document.getElementById(cardCount)
            card.classList.remove("fly-in")
        }
    }
}

function removeShuffleClasses()
{
    cards.forEach((card) => 
    {
        card.classList.remove("shuffle-left")
        card.classList.remove("shuffle-right")
    })
}

function animateShuffle(shuffleCount)
{
    const random1 = Math.floor(Math.random() * numCards) + 1
    const random2 = Math.floor(Math.random() * numCards) + 1

    let card1 = document.getElementById(random1)
    let card2 = document.getElementById(random2)

    if (shuffleCount % 4 == 0)
    {
        card1.classList.toggle("shuffle-left")
        card1.style.zIndex = 100
    }
    if (shuffleCount % 10 == 0)
    {
        card2.classList.toggle("shuffle-right")
        card2.style.zIndex = 200
    }
}

function shuffleCards()
{
    let shuffleCount = 0 
    const id = setInterval(shuffle, 12)

    function shuffle()
    {
        randomiseCardPositions()
        animateShuffle(shuffleCount)
        if(shuffleCount == 500)
        {
            clearInterval(id)
            shufflingInProgress = false
            removeShuffleClasses()
            dealCards()
            updateStatusElement(currentGameStateElem, "block", primaryColour, "Please click the card that you think is the ace of spades...")
        }
        else 
        {
            shuffleCount++
        }
    }

}

function randomiseCardPositions()
{
    const random1 = Math.floor(Math.random() * numCards) + 1
    const random2 = Math.floor(Math.random() * numCards) + 1
    const temp = cardPositions[random1 - 1]

    cardPositions[random1 - 1] = cardPositions[random2 - 1]
    cardPositions[random2 - 1] = temp
}

function dealCards()
{
    addCardsToAppropriateCell()
    const areasTemplate = returnGridAreasMappedToCardPos()
    transformGridArea(areasTemplate)
}

function returnGridAreasMappedToCardPos()
{
    let firstPart = ""
    let secondPart = ""
    let areas = ""

    cards.forEach((card, index) => 
    {
        if(cardPositions[index] == 1)
        {
            areas = areas + "a "
        }
        else if(cardPositions[index] == 2)
        {
            areas = areas + "b "
        }
        else if(cardPositions[index] == 3)
        {
            areas = areas + "c "
        }
        else if(cardPositions[index] == 4)
        {
            areas = areas + "d "
        }
        if(index == 1)
        {
            firstPart = areas.substring(0, areas.length - 1)
            areas = ""
        }
        else if(index == 3)
        {
            secondPart = areas.substring(0, areas.length - 1)
        }
    })

    return `"${firstPart}" "${secondPart}"`
}

function addCardsToAppropriateCell()
{
    cards.forEach((card) =>
    {
        addCardToGridCell(card)
    })
}

function createCards()
{
    cardObjectDefinitions.forEach((cardItem)=>
    {
        createCard(cardItem)
    })
}

function createCard(cardItem)
{   
    // creating div elements that house a card
    const cardElem = createElement('div')
    const cardInnerElem = createElement('div')
    const cardFrontElem = createElement('div')
    const cardBackElem = createElement('div')

    // creating image elements 
    const cardFrontImg = createElement('img')
    const cardBackImg = createElement('img')
    
    //adding class and id to card element
    addClassToElement(cardElem, 'card')
    addClassToElement(cardElem, 'fly-in')
    addIdToElement(cardElem, cardItem.id)

    //adding more classes
    addClassToElement(cardInnerElem, 'card-inner')
    addClassToElement(cardFrontElem, 'card-front')
    addClassToElement(cardBackElem, 'card-back')

    //adding source to back of card
    addSrcToImg(cardBackImg, cardBackImgPath)

    //adding source to front of cards, appropriately
    addSrcToImg(cardFrontImg, cardItem.imagePath)

    //adding class to images
    addClassToElement(cardFrontImg, 'card-img')
    addClassToElement(cardBackImg, 'card-img')

    //adding images as children of divs
    addChildElement(cardFrontElem, cardFrontImg)
    addChildElement(cardBackElem, cardBackImg)

    //adding front and back divs to inner div
    addChildElement(cardInnerElem, cardFrontElem)
    addChildElement(cardInnerElem, cardBackElem)

    //adding inner div to card div
    addChildElement(cardElem, cardInnerElem)

    //adding card to grid
    addCardToGridCell(cardElem)

    //adding card position
    initialiseCardPositions(cardElem)

    //adding event listener
    attachClickEventHandlerToCard(cardElem)
}

function attachClickEventHandlerToCard(card)
{
    card.addEventListener('click', () => chooseCard(card))
}

function initialiseCardPositions(card)
{
    cardPositions.push(card.id)
}

function createElement(elemType)
{
    return document.createElement(elemType)

}

function addClassToElement(elem, className)
{
    elem.classList.add(className)
}

function addIdToElement(elem, id)
{
    elem.id = id
}

function addSrcToImg(imgElem, src)
{
    imgElem.src = src
}

function addChildElement(parentElem, childElem)
{
    parentElem.appendChild(childElem)
}

function addCardToGridCell(card)
{
    const cardPositionClassName = mapCardIdToGridCell(card)
    const cardPosElem = document.querySelector(cardPositionClassName)

    addChildElement(cardPosElem, card)
}

function mapCardIdToGridCell(card)
{
    if(card.id == 1)
    {
        return '.card-pos-a'
    }
    else if(card.id == 2)
    {
        return '.card-pos-b'
    }
    else if(card.id == 3)
    {
        return '.card-pos-c'
    }
    else if(card.id == 4)
    {
        return '.card-pos-d'
    }
}

// local storage functions
function getSerialisedObjectAsJSON(obj)
{
    return JSON.stringify(obj)
}
function getObjectFromJSON(json)
{
    return JSON.parse(json)
}
function updateLocalStorageItem(key, value)
{
    localStorage.setItem(key, value)
}
function removeLocalStorageItem(key)
{
    localStorage.removeItem(key)
}
function getLocalStorageItemValue(key)
{
    return localStorage.getItem(key)
}
function updateGameObject(score, round)
{
    gameObj.score = score
    gameObj.round = round
}
function saveGameObjectToLocalStorage(score, round)
{
    updateGameObject(score, round)
    updateLocalStorageItem(localStorageGameKey, getSerialisedObjectAsJSON(gameObj))
}