// Global state
let currentPage = 'landing';
let selectedMood = localStorage.getItem('selectedMood');
let forumPosts = JSON.parse(localStorage.getItem('forumPosts')) || [];

// Motivational quotes
const quotes = [
    "You are stronger than you think and more capable than you imagine.",
    "Every small step forward is progress worth celebrating.",
    "Your mental health is just as important as your physical health.",
    "It's okay to not be okay. What matters is taking care of yourself.",
    "You don't have to be perfect. You just have to be you.",
    "Healing isn't linear, and that's perfectly normal.",
    "Your feelings are valid, and you deserve support and understanding."
];

// Sample forum posts
const samplePosts = [
    {
        id: "sample-1",
        title: "Dealing with exam anxiety",
        content: "Does anyone else feel overwhelmed when exam season approaches? I've been having trouble sleeping and my mind keeps racing. Any tips for managing this anxiety would be really helpful.",
        timestamp: "2 hours ago",
        replies: [
            {
                id: "reply-1",
                content: "I totally understand this feeling. What helped me was breaking down my study schedule into smaller chunks and taking regular breaks. Also, try some breathing exercises before bed.",
                timestamp: "1 hour ago"
            },
            {
                id: "reply-2",
                content: "The counseling center on campus offers free workshops on stress management. They really helped me develop better coping strategies.",
                timestamp: "45 minutes ago"
            }
        ]
    },
    {
        id: "sample-2",
        title: "Feeling isolated in my dorm",
        content: "It's my first year and I'm struggling to make friends. My roommate is always out and I spend most evenings alone. How do you meet people when you're naturally introverted?",
        timestamp: "5 hours ago",
        replies: [
            {
                id: "reply-3",
                content: "I felt the same way my first year! Try joining clubs related to your interests - it's easier to talk to people when you have something in common.",
                timestamp: "3 hours ago"
            }
        ]
    }
];

// Initialize sample posts if none exist
if (forumPosts.length === 0) {
    forumPosts = samplePosts;
    localStorage.setItem('forumPosts', JSON.stringify(forumPosts));
}

// Navigation functionality
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const heroButtons = document.querySelectorAll('.hero-buttons .btn');
    const tileButtons = document.querySelectorAll('.tile');
    const brandLogo = document.querySelector('.nav-brand');
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navLinksContainer = document.getElementById('navLinks');

    // Navigation click handlers
    function navigateToPage(pageName) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        
        // Show target page
        const targetPage = document.getElementById(pageName);
        if (targetPage) {
            targetPage.classList.add('active');
            currentPage = pageName;
        }
        
        // Update active nav link
        navLinks.forEach(link => link.classList.remove('active'));
        const activeLink = document.querySelector(`[data-page="${pageName}"]`);
        if (activeLink && activeLink.classList.contains('nav-link')) {
            activeLink.classList.add('active');
        }
    }

    // Nav link events
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const pageName = link.getAttribute('data-page');
            navigateToPage(pageName);
        });
    });

    // Hero button events
    heroButtons.forEach(button => {
        button.addEventListener('click', () => {
            const pageName = button.getAttribute('data-page');
            if (pageName) {
                navigateToPage(pageName);
            }
        });
    });

    // Tile button events
    tileButtons.forEach(tile => {
        tile.addEventListener('click', () => {
            const pageName = tile.getAttribute('data-page');
            if (pageName && pageName !== '#') {
                navigateToPage(pageName);
            }
        });
    });

    // Brand logo click
    brandLogo.addEventListener('click', () => {
        navigateToPage('landing');
    });

    // Mobile menu toggle
    mobileMenuBtn.addEventListener('click', () => {
        navLinksContainer.classList.toggle('show');
    });
}

// Mood tracking functionality
function initMoodTracker() {
    const moodButtons = document.querySelectorAll('.mood-button');
    const moodFeedback = document.getElementById('moodFeedback');

    // Load saved mood
    if (selectedMood) {
        const savedMoodButton = document.querySelector(`[data-mood="${selectedMood}"]`);
        if (savedMoodButton) {
            savedMoodButton.classList.add('selected');
            showMoodFeedback(selectedMood);
        }
    }

    moodButtons.forEach(button => {
        button.addEventListener('click', () => {
            const moodValue = button.getAttribute('data-mood');
            
            // Remove previous selection
            moodButtons.forEach(btn => btn.classList.remove('selected'));
            
            // Add selection to clicked button
            button.classList.add('selected');
            
            // Save mood to localStorage
            selectedMood = moodValue;
            localStorage.setItem('selectedMood', moodValue);
            
            // Show feedback
            showMoodFeedback(moodValue);
        });
    });

    function showMoodFeedback(mood) {
        const feedbackMessages = {
            'happy': "Great to see you're feeling positive! Keep up the good energy.",
            'neutral': "It's okay to feel neutral. Every day doesn't have to be amazing.",
            'sad': "It's important to acknowledge when you're feeling down. Consider reaching out for support.",
            'very-sad': "You're going through a tough time. Please consider talking to someone you trust.",
            'angry': "Anger is a valid emotion. Try some breathing exercises or physical activity to help process these feelings."
        };

        if (moodFeedback && feedbackMessages[mood]) {
            moodFeedback.textContent = feedbackMessages[mood];
            moodFeedback.classList.add('show', 'fade-in');
        }
    }
}

// Motivational quotes functionality
function initQuotes() {
    const quoteElement = document.getElementById('motivationalQuote');
    const newQuoteBtn = document.getElementById('newQuoteBtn');

    function changeQuote() {
        const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
        if (quoteElement) {
            quoteElement.textContent = `"${randomQuote}"`;
            quoteElement.classList.add('fade-in');
            setTimeout(() => quoteElement.classList.remove('fade-in'), 300);
        }
    }

    if (newQuoteBtn) {
        newQuoteBtn.addEventListener('click', changeQuote);
    }

    // Set initial quote
    changeQuote();
}

// Forum functionality
function initForum() {
    const postTitleInput = document.getElementById('postTitle');
    const postContentInput = document.getElementById('postContent');
    const sharePostBtn = document.getElementById('sharePostBtn');
    const postsContainer = document.getElementById('postsContainer');

    function renderPosts() {
        if (!postsContainer) return;
        
        postsContainer.innerHTML = '';
        
        forumPosts.forEach(post => {
            const postElement = createPostElement(post);
            postsContainer.appendChild(postElement);
        });
    }

    function createPostElement(post) {
        const postDiv = document.createElement('div');
        postDiv.className = 'forum-post';
        postDiv.setAttribute('data-testid', `post-${post.id}`);
        
        postDiv.innerHTML = `
            <h3>${escapeHtml(post.title)}</h3>
            <div class="forum-post-content">${escapeHtml(post.content)}</div>
            <div class="forum-post-meta">
                <span>${post.timestamp}</span>
                <button class="replies-toggle" data-post-id="${post.id}" data-testid="button-toggle-replies-${post.id}">
                    ${post.replies.length > 0 ? 'Show' : 'No'} ${post.replies.length} replies
                </button>
            </div>
            <div class="forum-replies hidden" id="replies-${post.id}" data-testid="replies-${post.id}">
                ${post.replies.map(reply => `
                    <div class="forum-reply">
                        <div class="forum-reply-content">${escapeHtml(reply.content)}</div>
                        <div class="forum-reply-time">${reply.timestamp}</div>
                    </div>
                `).join('')}
            </div>
        `;

        // Add event listener for replies toggle
        const repliesToggle = postDiv.querySelector('.replies-toggle');
        const repliesContainer = postDiv.querySelector('.forum-replies');
        
        if (repliesToggle && repliesContainer && post.replies.length > 0) {
            repliesToggle.addEventListener('click', () => {
                const isHidden = repliesContainer.classList.contains('hidden');
                repliesContainer.classList.toggle('hidden');
                repliesToggle.textContent = `${isHidden ? 'Hide' : 'Show'} ${post.replies.length} replies`;
            });
        }

        return postDiv;
    }

    function createPost() {
        const title = postTitleInput?.value.trim();
        const content = postContentInput?.value.trim();

        if (title && content) {
            const newPost = {
                id: Date.now().toString(),
                title: title,
                content: content,
                timestamp: "Just now",
                replies: []
            };

            forumPosts.unshift(newPost);
            localStorage.setItem('forumPosts', JSON.stringify(forumPosts));
            
            // Clear inputs
            if (postTitleInput) postTitleInput.value = '';
            if (postContentInput) postContentInput.value = '';
            
            // Re-render posts
            renderPosts();
        }
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Event listeners
    if (sharePostBtn) {
        sharePostBtn.addEventListener('click', createPost);
    }

    // Enable/disable share button based on input
    function updateShareButton() {
        if (sharePostBtn && postTitleInput && postContentInput) {
            const hasTitle = postTitleInput.value.trim().length > 0;
            const hasContent = postContentInput.value.trim().length > 0;
            sharePostBtn.disabled = !(hasTitle && hasContent);
        }
    }

    if (postTitleInput) {
        postTitleInput.addEventListener('input', updateShareButton);
    }
    if (postContentInput) {
        postContentInput.addEventListener('input', updateShareButton);
    }

    // Initial render
    renderPosts();
    updateShareButton();
}

// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initMoodTracker();
    initQuotes();
    initForum();
    
    // Handle resource buttons (dummy functionality)
    document.querySelectorAll('[data-testid^="button-read-more"]').forEach(button => {
        button.addEventListener('click', () => {
            alert('This would open detailed resources in a real application!');
        });
    });

    // Handle SOS button
    const sosButton = document.querySelector('[data-testid="button-sos"]');
    if (sosButton) {
        sosButton.addEventListener('click', () => {
            alert('In a real emergency, this would immediately connect you to crisis support services.');
        });
    }
});

// Utility functions
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
        console.error('Error saving to localStorage:', error);
    }
}

function getFromLocalStorage(key, defaultValue = null) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
        console.error('Error reading from localStorage:', error);
        return defaultValue;
    }
}