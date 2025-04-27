document.addEventListener('DOMContentLoaded', function() {
    // Initialize Cytoscape
    const cy = cytoscape({
        container: document.getElementById('cy'),
        elements: graphData,
        style: [
            {
                selector: 'node',
                style: {
                    'background-color': 'data(color)',
                    'label': 'data(label)',
                    'color': '#fff',
                    'text-outline-color': '#000',
                    'text-outline-width': 2,
                    'font-size': '14px',
                    'width': 50,
                    'height': 50
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 2,
                    'line-color': '#4b5563',
                    'target-arrow-color': '#4b5563',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'label': 'data(label)',
                    'color': '#9ca3af',
                    'font-size': '12px'
                }
            }
        ],
        layout: {
            name: 'cose',
            padding: 50,
            animate: true,
            animationDuration: 1000,
            nodeDimensionsIncludeLabels: true
        }
    });

    // Navigation Handling
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('bg-gray-700'));
            // Add active class to clicked link
            link.classList.add('bg-gray-700');
            
            // Update header title
            const headerTitle = document.querySelector('header h2');
            headerTitle.textContent = link.querySelector('span').textContent;
            
            // Handle section visibility (to be implemented with actual sections)
        });
    });

    // Zoom Controls
    document.getElementById('zoomIn').addEventListener('click', () => {
        cy.zoom({
            level: cy.zoom() * 1.2,
            renderedPosition: { x: cy.width() / 2, y: cy.height() / 2 }
        });
    });

    document.getElementById('zoomOut').addEventListener('click', () => {
        cy.zoom({
            level: cy.zoom() * 0.8,
            renderedPosition: { x: cy.width() / 2, y: cy.height() / 2 }
        });
    });

    document.getElementById('reset').addEventListener('click', () => {
        cy.fit();
        cy.center();
    });

    // Node Selection
    cy.on('tap', 'node', function(evt) {
        const node = evt.target;
        showNodeDetails(node);
    });

    // Click outside to clear selection
    cy.on('tap', function(evt) {
        if (evt.target === cy) {
            hideNodeDetails();
        }
    });

    // Node Details Panel
    function showNodeDetails(node) {
        // Create a modal for node details
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 z-50 flex items-center justify-center';
        modal.innerHTML = `
            <div class="modal-backdrop"></div>
            <div class="modal-content p-6 w-96">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-lg font-semibold">Node Details</h3>
                    <button class="text-gray-400 hover:text-white close-modal">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="space-y-4">
                    <div>
                        <label class="text-sm text-gray-400">Type</label>
                        <p class="text-white">${node.data('type')}</p>
                    </div>
                    <div>
                        <label class="text-sm text-gray-400">Label</label>
                        <p class="text-white">${node.data('label')}</p>
                    </div>
                    <div>
                        <label class="text-sm text-gray-400">Connections</label>
                        <p class="text-white">${node.neighborhood().length}</p>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Close modal handler
        modal.querySelector('.close-modal').addEventListener('click', () => {
            document.body.removeChild(modal);
        });

        modal.querySelector('.modal-backdrop').addEventListener('click', () => {
            document.body.removeChild(modal);
        });
    }

    function hideNodeDetails() {
        const modal = document.querySelector('.modal-content');
        if (modal) {
            modal.parentElement.remove();
        }
    }

    // Web3 Connect Button
    const connectWalletBtn = document.querySelector('button.mt-2.bg-purple-600');
    if (connectWalletBtn) {
        connectWalletBtn.addEventListener('click', async () => {
            if (typeof window.ethereum !== 'undefined') {
                try {
                    await window.ethereum.request({ method: 'eth_requestAccounts' });
                    // Update UI to show connected state
                    updateWalletUI(true);
                } catch (error) {
                    console.error('User denied account access');
                }
            } else {
                alert('Please install MetaMask to use Web3 features');
            }
        });
    }

    function updateWalletUI(connected) {
        const walletStatus = document.querySelector('.text-xs.text-gray-400');
        if (connected) {
            walletStatus.textContent = 'Connected';
            walletStatus.classList.remove('text-gray-400');
            walletStatus.classList.add('text-green-500');
        }
    }

    // Initial layout
    cy.layout({ name: 'cose' }).run();
});
