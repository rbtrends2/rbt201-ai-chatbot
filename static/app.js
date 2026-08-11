const form = document.querySelector("#chat-form");
const question = document.querySelector("#question");
const status = document.querySelector("#status");
const answerPanel = document.querySelector("#answer-panel");
const answer = document.querySelector("#answer");
const provider = document.querySelector("#provider");
const citations = document.querySelector("#citations");
const sampleQuestion = document.querySelector("#sample-question");
const submitButton = form.querySelector("button[type='submit']");

sampleQuestion.addEventListener("click", () => {
  question.value = "What makes a RAG answer trustworthy?";
  question.focus();
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const value = question.value.trim();
  if (!value) {
    status.textContent = "Enter a question first.";
    return;
  }

  submitButton.disabled = true;
  status.textContent = "Retrieving sources and drafting an answer...";
  answerPanel.hidden = true;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question: value}),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "The chatbot could not answer.");
    }

    answer.textContent = payload.answer;
    provider.textContent = payload.provider;
    citations.replaceChildren();
    payload.citations.forEach((citation) => {
      const item = document.createElement("li");
      const title = document.createElement("strong");
      title.textContent = `${citation.title} (${citation.source})`;
      const excerpt = document.createElement("span");
      excerpt.textContent = citation.excerpt;
      item.append(title, excerpt);
      citations.append(item);
    });
    answerPanel.hidden = false;
    status.textContent = payload.grounded
      ? "Answer grounded in retrieved sources."
      : "No matching sources were found.";
  } catch (error) {
    status.textContent = error instanceof Error
      ? error.message
      : "The chatbot could not answer.";
  } finally {
    submitButton.disabled = false;
  }
});
