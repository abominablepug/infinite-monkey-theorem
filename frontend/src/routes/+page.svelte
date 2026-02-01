<script lang="ts">
	import { onMount } from 'svelte';
	import { env } from '$env/dynamic/public';

	let popupOpen = $state(false);
	let typedText = $state("");
	let status = $state("Disconnected");
	let tokens = $state<{ type: string, text: string }[]>([]);

	let socket: WebSocket;

	onMount(() => {
		const socketUrl = env.PUBLIC_BACKEND_URL;
		socket = new WebSocket(socketUrl);

		socket.onmessage = (event) => {
			try {
				if (event.data.startsWith('{')) {
					const data = JSON.parse(event.data);
					tokens.push(data);
					if (tokens.length > 500) tokens.shift();
				} else {
					typedText += event.data;
					if (typedText.length > 5000) typedText = typedText.slice(-5000);
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

<main class="min-h-screen bg-slate-950 text-slate-200 p-8 font-mono">
	<div class="max-w-4xl mx-auto space-y-6">
		<header class="flex justify-between items-center border-b border-slate-800 pb-4">
			<h1 class="text-2xl font-bold bg-gradient-to-r from-purple-600 to-purple-600 bg-clip-text text-transparent">
				Infinite Monkey Theorem
			</h1>
			<div class="flex items-center gap-2">
				<div class="w-3 h-3 rounded-full {status === "Connected" ? "bg-emerald-500 animate-pulse" : "bg-red-500"}"></div>
				<span class="text-sm font-medium uppercase tracking-widest">{status}</span>
			</div>
		</header>

		<div class="flex flex-wrap gap-3">
			<button onclick={() => toggle('start')} class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-md transition-colors font-bold text-slate-950">
				Give Typewriter to Monkey 🐵
			</button>
			<button onclick={() => toggle('stop')} class="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-md transition-colors">
				Take Typewriter Away 🙊
			</button>
			<button onclick={() => popupOpen = true} class="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 rounded-md transition-colors">
				Show Found Words ({tokens.length}) 🙈
			</button>
			<button onclick={() => { typedText = ""; }} class="px-4 py-2 border border-slate-700 hover:bg-slate-800 rounded-md transition-colors">
				Reset 🙉
			</button>
		</div>

		<div class="relative bg-black rounded-xl border border-slate-800 p-6 shadow-2xl h-96 overflow-y-auto break-all scrollbar-thin scrollbar-thumb-slate-800">
			<div class="text-emerlad-500/80 leading-relaxed">
				{typedText}
				<span class="inline-block w-1 h-4 bg-emerald-500 animate-pulse ml-1"></span>
			</div>
		</div>

		{#if popupOpen}
			<div class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
				<div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-fulll max-h-[70vh] flex flex-col shadow-2xl">
					<div class="p-6 border-b border-slate-800 flex justify-between items-center">
						<h2 class="text-xl font-bold text-cyan-400">Words Discovered</h2>
						<button onclick={() => popupOpen = false} class="text-slate-400 hover:text-white">x</button>
					</div>

					<div class="p-6 overflow-y-auto flex flex-wrap gap-2">
						{#if tokens.length === 0}
							<p class="text-slate-500 italic">No human language detected yet.</p>
						{:else}
							{#each tokens as token}
								<span class="px-3 py-1 bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 rounded-full text-sm">
									{token.text}
								</span>
							{/each}
						{/if}
					</div>

					<div class="p-4 bg-slate-950/50 text-right rounded-b-2xl">
						<button onclick={() => popupOpen = false} class="px-6 py-2 bg-slate-800 hover:bg-slate-700 rounded-sm">
							Close
						</button>
					</div>
				</div>
			</div>
		{/if}
	</div>
</main>

<style>
.scrollbar-thin::-webkit-scrollbar {
	width: 8px;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
	background: #1e293b;
	border-radius: 10px;
}
</style>
