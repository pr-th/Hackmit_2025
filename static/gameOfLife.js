let player = {
    age: 18,
    stage: "College",
    income: 0,
    savings: 0,
    balance: 10000, 
    debt: 0,
    expenses: 0,
    choicesMade: {},
    currentJob: "",
    salary: 0,
    passiveIncome: 0
};




let choicesMade = 0;
let stageAges = { "College": 18, "First Job": 23, "Marriage": 30, "Retirement": 60 };

const lifeStages = {
    "College": {
        income: 0,
        expenses: 500,
        choices: [
            { text: "Take a student loan", unlimited: true },
            { text: "Work part-time", limit: 2 },
            { text: "Live frugally", limit: 3 }
        ]
    },
    "First Job": {
        income: 3000,
        expenses: 1500,
        choices: [
            { text: "Save aggressively", limit: 1 },
            { text: "Invest in stocks", limit: 3 },
            { text: "Work full-time", limit: 2 }
        ]
    },
    "Marriage": {
        income: 5000,
        expenses: 4000,
        choices: [
            { text: "Buy a house", limit: 1 },
            { text: "Rent and save", limit: 2 },
            { text: "Luxury lifestyle", limit: 2 }
        ]
    },
    "Retirement": {
        income: 2000,
        expenses: 1500,
        choices: [
            { text: "Rely on savings", limit: 3 },
            { text: "Invest in passive income", limit: 3 },
            { text: "Work part-time", limit: 1 }
        ]
    }
};

const partTimeJobs = {
    "College": [
        { name: "Pizza Delivery", income: 500 },
        { name: "Intern", income: 800 },
        { name: "Paper Delivery", income: 400 },
        { name: "Tutor", income: 700 }
    ],
    "First Job": [
        { name: "Freelance Developer", income: 1500 },
        { name: "Uber Driver", income: 1200 },
        { name: "Online Tutor", income: 1000 }
    ],
    "Retirement": [
        { name: "Consultant", income: 1000 },
        { name: "Bookstore Clerk", income: 600 },
        { name: "Freelance Writer", income: 800 }
    ]
};



const events = [
    { message: "Stock market crashed! Huge losses incurred. Portfolio down by 8%.", impact: -800 },
    { message: "Great day! Earned a total profit of 12% on investments.", impact: 1200 },
    { message: "Phew! That was close! Took a loss, but only 3% down.", impact: -300 },
    { message: "Not a great day, but good enough. Managed a small 4% profit.", impact: 400 },
    { message: "Tech stocks skyrocketed! Portfolio up by 15%!", impact: 1500 },
    { message: "A bad day for the markets. A 6% dip hit hard.", impact: -600 },
    { message: "Surprising market rebound! Earned a quick 7% profit.", impact: 700 },
    { message: "Major sell-off! Lost 10% of portfolio value.", impact: -1000 },
    { message: "Steady gains! Portfolio climbed by 5%.", impact: 500 },
    { message: "A volatile session, but ended up with a 2% gain.", impact: 200 },
    { message: "Inflation fears spooked the market. Lost 4%.", impact: -400 },
    { message: "Earnings season boost! Gained 9% today.", impact: 900 },
    { message: "Regulatory changes hurt the market. Dropped 7%.", impact: -700 },
    { message: "A surprising rally! Unexpected 13% profit!", impact: 1300 },
    { message: "A tough day. Stocks fell, resulting in a 5% loss.", impact: -500 },
    { message: "Safe bets paid off! A steady 6% gain.", impact: 600 },
    { message: "Sector rotation in play! Your stocks are up by 8%.", impact: 800 },
    { message: "Heavy volatility! Despite the swings, gained 3%.", impact: 300 },
    { message: "Fed policy announcement shook the market. Lost 9%.", impact: -900 },
    { message: "A mixed day, but still managed a small 1% profit.", impact: 100 }
];


function startGame() {
    player.stage = "College";
    player.age = stageAges[player.stage];
    choicesMade = 0;
    updateUI();
}

function triggerRandomEvent() {
    const event = events[Math.floor(Math.random() * events.length)];
    player.balance += event.impact; // Apply directly to balance
    alert(event.message);
    updateUI();
}

function makeChoice(choice) {
    // If the choice is not "Buy a house", hide the house options
    if (choice !== "Buy a house") {
        document.getElementById("houseOptions").style.display = "none";
    }

    let stageData = lifeStages[player.stage];
    let selectedChoice = stageData.choices.find(c => c.text === choice);
    
    // Check if the choice has a limit
    if (!selectedChoice.unlimited) {
        if (!player.choicesMade[choice]) player.choicesMade[choice] = 0;
        if (player.choicesMade[choice] >= selectedChoice.limit) {
            alert("You can't choose this option anymore!");
            return;
        }
        player.choicesMade[choice]++;
    }

    applyChoiceEffects(choice);
    choicesMade++;
    player.age++;

    if (choicesMade === 5) {
        setTimeout(nextStage, 500);
    }

    updateUI();
}


function applyChoiceEffects(choice) {
    if (choice === "Take a student loan") {
        player.debt += 10000;
        player.balance -= 10000; // Deduct loan amount immediately
    }
    if (choice === "Live frugally") {
        player.balance -= 500;
    }
    if (choice === "Save aggressively") {
        player.balance -= 1000;
    }
    if (choice === "Invest in stocks") {
        triggerRandomEvent();
        // Let it fall through so that the general update still occurs.
    }
    if (choice === "Buy a house") {
        showHouseOptions();
        return; // Let the house selection handle its own update.
    }
    if (choice === "Rent and save") {
        player.balance -= 2000;
    }
    if (choice === "Luxury lifestyle") {
        player.balance -= 3000;
    }
    if (choice === "Work part-time" || choice === "Work full-time") {
        assignPartTimeJob();
        // Do NOT return; allow the general update below to add the yearly income.
    }
    if (choice === "Invest in passive income") {
        investInPassiveIncome();
    }
    if (choice === "Rely on savings") {
        player.balance -= 3000;
    }

    // General update: simulate a year's progress.
    player.balance += (player.income * 12) + player.passiveIncome - player.expenses;
    
    // Check for bankruptcy immediately.
    if (player.balance < 0) {
        gameOver(player.balance);
        return;
    }

    moveWalkingMan();
    updateUI();
}




function showHouseOptions() {
    document.getElementById("houseOptions").style.display = "block";
}

function buyHouse(debt, incomeIncrease) {
    player.debt += debt; 
    player.balance -= debt; // Deduct house cost immediately
    player.income += incomeIncrease; // Increase income if applicable

    // Hide house selection buttons after selection
    document.getElementById("houseOptions").style.display = "none";
    
    updateUI();
    moveWalkingMan();
    // Immediately check if balance is negative
    if (player.balance < 0) {
        gameOver(player.balance);
        return;
    }
    
}



function investInPassiveIncome() {
    let investment = player.balance * 0.3;
    
    if (investment > 0) {
        player.balance -= investment;
        let passiveGain = Number((investment * 0.1).toFixed(2));
        player.passiveIncome += passiveGain;
    }
}



function resetGame() {
    player.age = 17;
    player.stage = "College";
    player.income = 0;
    player.savings = 0;
    player.balance = 10000;
    player.debt = 0;
    player.expenses = 0;
    player.choicesMade = {}; 
    player.currentJob = "";
    player.passiveIncome = 0;

    choicesMade = 0; 

    progressPercent = 0;
    stepCount = 0;
    stageIndex = 0;

    const walkingMan = document.getElementById("walkingMan");
    walkingMan.style.left = "0px";
    walkingMan.src = window.imagePaths ? window.imagePaths[0] : "static/young.png";

    updateUI();
}




   
function assignPartTimeJob() {
    let k = player.salary;
    let jobs = partTimeJobs[player.stage];
    let randomJob = jobs[Math.floor(Math.random() * jobs.length)];

    // Set the new salary and job details
    player.salary = randomJob.income;
    player.income = player.income + player.salary - k;
    
    player.currentJob = `${randomJob.name} ($${randomJob.income})`;

    updateUI();
}




function nextStage() {
    choicesMade = 0;

    if (player.stage === "College") {
        player.stage = "First Job";
    } 
    else if (player.stage === "First Job") {
        player.stage = "Marriage";
    } 
    else if (player.stage === "Marriage") {
        player.stage = "Retirement";
        player.income -= player.salary; 
        player.currentJob = ""; 
    } 
    else {
        gameOver(player.balance);
        return;
    }

    player.age = stageAges[player.stage];
    player.choicesMade = {};
    
    updateUI(); // UI updates properly
}




updateUI();

function updateUI() {
    document.getElementById("age").innerText = "Age: " + player.age;
    document.getElementById("income").innerText = "Income: $" + player.income;
    document.getElementById("debt").innerText = "Debt: $" + player.debt;
    document.getElementById("balance").innerText = "Balance: $" + player.balance;
    document.getElementById("passiveIncome").innerText = "Passive Income: $" + player.passiveIncome;
    document.getElementById("stage").innerText = "Life Stage: " + player.stage;
    document.getElementById("job").innerText = player.currentJob ? `Job-Type: ${player.currentJob}` : "Job: None";

    const choicesContainer = document.getElementById("choices");
    choicesContainer.innerHTML = ""; 

    lifeStages[player.stage].choices.forEach(choice => {
        const button = document.createElement("button");
        button.innerText = choice.text;
        button.onclick = () => makeChoice(choice.text);

        // Instead of disabling the button, add a visual cue (class) if limit is reached.
        if (!choice.unlimited && player.choicesMade[choice.text] >= choice.limit) {
            button.classList.add("disabled-choice");
        }

        choicesContainer.appendChild(button);
    });
}


// Walking Man Mechanics

let mainContent;


document.addEventListener("DOMContentLoaded", function () {
    const walkingMan = document.getElementById("walkingMan");
    mainContent = document.getElementById("main-content");

    if (!mainContent) {
        console.error("main-content div not found!");
        return;
    }

    // function setInitialPosition() {
    //     walkingMan.style.left = mainContent.offsetLeft + "px";
    // }

    // setInitialPosition();
});
  

let progressPercent = 0;  
let stepCount = 0;        
let stageIndex = 0;      

const images = window.imagePaths; 
// 

function moveWalkingMan() {
    if (!mainContent) {
        console.error("mainContent is not found!");
        return;
    }

    progressPercent += 5;
    console.log("Moving man to: " + ( (mainContent.offsetWidth * (progressPercent / 100))) + "px");

    walkingMan.style.left = ( (mainContent.offsetWidth * (progressPercent / 100))) + "px";

    stepCount++;
    if (stepCount === 5) {
        stepCount = 0;
        if (stageIndex < images.length - 1) {
            stageIndex++;
            walkingMan.src = images[stageIndex];
        }
    }
}

// gameOver functions

function gameOver(finalAmount) {
    let modal = document.getElementById("gameOverModal");
    let message = document.getElementById("finalMessage");
    let balance = document.getElementById("finalBalance");

    if (finalAmount > 10000) {
        message.innerText = "Amazing! You made a fortune!";
    } else if (finalAmount > 5000) {
        message.innerText = "Great job! You played it safe and earned well!";
    } else if (finalAmount > 1000) {
        message.innerText = "Not bad! You made some gains!";
    } else if (finalAmount > 0) {
        message.innerText = "Phew! At least you didn’t lose everything!";
    } else {
        message.innerText = "Ouch! The choices you made weren't in your favor.";
    }

    balance.innerText = `Final Balance: $${finalAmount}`;
    modal.style.display = "block";
}

function restartGame() {
    document.getElementById("gameOverModal").style.display = "none";
    resetGame();
    return;
}
