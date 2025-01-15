import java.util.*;

class Main {
	public static void knapsackGreProc(int W[], int V[], int M, int n) {
		KnapsackPackage[] packs = new KnapsackPackage[n];
		for (int i = 0; i < n; i++) {
			packs[i] = new KnapsackPackage(W[i], V[i]);
		}

		Arrays.sort(packs, new Comparator<KnapsackPackage>() {
			@Override
			public int compare(KnapsackPackage kPackA, KnapsackPackage kPackB) {
				return kPackB.getCost().compareTo(kPackA.getCost());
			}
		});

		int remain = M;
		double result = 0d;

		int i = 0;
		boolean stopProc = false;
		while (!stopProc) {
			if (packs[i].getWeight() <= remain) {
				remain -= packs[i].getWeight();
				result += packs[i].getValue();

				System.out
						.println("Pack " + i + " - Weight " + packs[i].getWeight() + " - Value " + packs[i].getValue());
			}

			if (packs[i].getWeight() > remain) {
				i++;
			}

			if (i == n) {
				stopProc = true;
			}
		}

		System.out.println("Max Value:\t" + result);
	}

	public static void run() {
		/*
		 * Pack and Weight - Value
		 */
		// int W[] = new int[]{15, 10, 2, 4};
		int V[] = new int[] { 15, 32, 3, 12 };

		// int V[] = new int[]{30, 25, 2, 6};
		int W[] = new int[] { 3,8,1,2 };

		/*
		 * Max Weight
		 */
		// int M = 37;
		int M = 9;
		int n = V.length;

		/*
		 * Run the algorithm
		 */
		knapsackGreProc(W, V, M, n);
	}

	public static void main(String[] args) {
		run();
	}
}
class KnapsackPackage {
	
	private double weight;
	private double value;
	private Double cost;
	
	public KnapsackPackage(double weight, double value) {
		super();
		
		this.weight = weight;
		this.value = value;
		this.cost = new Double(value / weight);
	}

	public double getWeight() {
		return weight;
	}

	public double getValue() {
		return value;
	}

	public Double getCost() {
		return cost;
	}

}