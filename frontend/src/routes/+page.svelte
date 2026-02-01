<script lang="ts">
	import { onMount } from 'svelte';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';

	let popupOpen = $state(false);
	let typedText = $state("");
	let status = $state("Disconnected");
	let tokens = $state<{ type: string, text: string }[]>([]);

	let socket: WebSocket;

	onMount(() => {
		socket = new WebSocket(PUBLIC_BACKEND_URL);

		socket.onmessage = (event) => {
			try {
				if (event.data.startsWith('{')) {
					const data = JSON.parse(event.data);
					tokens.push(data);
					if (tokens.length > 500) tokens.shift();
				} else {
					typedText += event.data;
				}
			} catch (e) {
				console.error("Error parsing message:", e);
			}
		};

		socket.onopen = () => {
			status = "Connected";
		};
		socket.onclose = () => {
			status = "Disconnected";
		};
	});

	const toggle = (cmd: string) => {
		if (socket && socket.readyState === WebSocket.OPEN) {
			socket.send(cmd);
		}
	};


</script>

<main>
	<h1>Infinite Monkey Dashboard</h1>
	<p>Status: {status}</p>

	<div>
		<button onclick={() => toggle('start')}>Start Typing</button>
		<button onclick={() => toggle('stop')}>Stop Typing</button>
		<button onclick={() => popupOpen = true}>Show Found Words</button>
		<button onclick={() => typedText = ""}>Reset</button>
	</div>

	<div>{typedText}</div>

	{#if popupOpen}
		<div>
			<div>
				<div>
					<h2>Words Discovered</h2>
					<button onclick={() => popupOpen = false}>x</button>
				</div>

				<div>
					{#if tokens.length === 0}
						<p>No human language detected yet.</p>
					{:else}
						{#each tokens as token}
							{#if token.type === 'word'}
								<p>{token.text}</p>
							{/if}
						{/each}
					{/if}
				</div>
			</div>
		</div>
	{/if}
</main>
