let player = {
    age: 18,
    stage: "College",
    income: 0,
    savings: 0,
    balance: 1000, 
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
    player.savings += event.impact;
    alert(event.message);
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
    if (choice === "Take a student loan") player.debt += 5000;
    if (choice === "Live frugally") player.expenses -= 200;
    if (choice === "Save aggressively") player.savings += 1000;
    if (choice === "Invest in stocks") triggerRandomEvent();
    if (choice === "Buy a house") {
        player.debt += 100000;
        player.income += 1000; 
    }
    if (choice === "Rent and save") player.savings += 2000;
    if (choice === "Luxury lifestyle") player.expenses += 3000;
    if (choice === "Work part-time" || choice === "Work full-time") assignPartTimeJob();
    if (choice === "Invest in passive income") investInPassiveIncome();

    updateBalance();
}

function investInPassiveIncome() {
    let investment = player.balance * 0.3;

    if (investment > 0) {
        player.balance -= investment; // Deduct 30% of balance
        player.passiveIncome += investment * 0.05; // Set yearly passive income
    }
}


function updateBalance() {
    player.balance += (player.income * 12) + player.passiveIncome - player.debt - player.expenses;

    if (player.balance < 0) {
        alert("Game Over! You went bankrupt! 😢");
        resetGame();
        return;
    }

    updateUI();
}


function resetGame() {
    player.age = 18;
    player.stage = "College";
    player.income = 0;
    player.savings = 0;
    player.balance = 1000;
    player.debt = 0;
    player.expenses = 0;
    player.choicesMade = 0;
    player.currentJob = "";

    updateUI();
}




   
function assignPartTimeJob() {
    let jobs = partTimeJobs[player.stage];
    let randomJob = jobs[Math.floor(Math.random() * jobs.length)];

    player.income += randomJob.income;
    player.currentJob = `${randomJob.name} ($${randomJob.income})`;

    updateUI();
}



function nextStage() {
    choicesMade = 0;

    if (player.stage === "College") {
        player.stage = "First Job";
        player.income += 3000;
        player.debt += 5000;
    } 
    else if (player.stage === "First Job") {
        player.stage = "Marriage";
        player.income += 5000;
        player.debt += 10000;
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
    updateUI();
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
