let player = {
    age: 18,
    stage: "College",
    income: 0,
    savings: 0,
    balance: 10000, 
    debt: 0,
    expenses: 0,
    choicesMade: 0,
    currentJob: "",
    passiveIncome: 0 // New attribute
};



let choicesMade = 0;
let stageAges = { "College": 18, "First Job": 23, "Marriage": 30, "Retirement": 60 };

const lifeStages = {
    "College": {
        income: 0,
        expenses: 500,
        choices: [
            { text: "Take a student loan", limit: 1 },
            { text: "Work part-time", unlimited: true },
            { text: "Live frugally", limit: 3 }
        ]
    },
    "First Job": {
        income: 3000,
        expenses: 1500,
        choices: [
            { text: "Save aggressively", limit: 2 },
            { text: "Invest in stocks", limit: 3 },
            { text: "Work full-time", unlimited: true }
        ]
    },
    "Marriage": {
        income: 5000,
        expenses: 4000,
        choices: [
            { text: "Buy a house", limit: 1 },
            { text: "Rent and save", limit: 3 },
            { text: "Luxury lifestyle", limit: 2 }
        ]
    },
    "Retirement": {
        income: 2000,
        expenses: 1500,
        choices: [
            { text: "Rely on savings", limit: 3 },
            { text: "Invest in passive income", limit: 3 },
            { text: "Work part-time", unlimited: true }
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
    { message: "Unexpected medical bill! Lose $1000.", impact: -1000 },
    { message: "Bonus at work! Gain $2000.", impact: 2000 },
    { message: "Stock market crash! Lose $500.", impact: -500 },
    { message: "Side hustle success! Gain $1500.", impact: 1500 },
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
        alert("Game Over! You went bankrupt! 😢");
        resetGame();
        return;
    }
    
    updateUI();
    moveWalkingMan();
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
        alert("Game Over! You went bankrupt! 😢");
        resetGame();
        return;
    }
    
}



function investInPassiveIncome() {
    let investment = player.balance * 0.3;
    
    if (investment > 0) {
        player.balance -= investment; // Deduct investment amount immediately
        player.passiveIncome += investment * 0.1; // Add yearly passive income
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
    player.choicesMade = 0; // ✅ Reset to 0 (integer)
    player.currentJob = "";
    player.passiveIncome = 0;

    choicesMade = 0; // ✅ Also reset global choicesMade counter

    updateUI();
}




   
function assignPartTimeJob() {
    let jobs = partTimeJobs[player.stage];
    let randomJob = jobs[Math.floor(Math.random() * jobs.length)];

    // Set the new salary and job details
    player.income = randomJob.income;
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
        player.income = 0; 
        player.currentJob = ""; 
    } 
    else {
        alert("Game Over! Your final balance: $" + player.balance);
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

        // Disable button if limit is reached
        if (!choice.unlimited && player.choicesMade[choice.text] >= choice.limit) {
            button.disabled = true;
        }

        choicesContainer.appendChild(button);
    });
}


// Walking Man Mechanics

let progressPercent = 0;  
let stepCount = 0;        
let stageIndex = 0;      

const walkingMan = document.getElementById("walkingMan");
const images = window.imagePaths; 

function moveWalkingMan() {
    progressPercent += 5;
    walkingMan.style.left = progressPercent + "%";
    stepCount++;
    if (stepCount >= 5) {
        stepCount = 0;
        if (stageIndex < images.length - 1) {
        stageIndex++;
            walkingMan.src = images[stageIndex];
        }
    }
}