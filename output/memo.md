LIQUID AI  /  PRODUCT PROPOSAL  /  FUAD ALI

## Recovery for packaging machines

An operator switches products. The machine stops, they check the product settings, and it stops again with the same alarm. I would build Recovery to show the next useful check using the manufacturer’s instructions and what the operator already tried. The equipment maker’s service team would buy it.

### The first customer and problem

* Start with one family of case packing machines, without robots, and two common stops after a product change. The first user is an operator or maintenance technician who needs to know which check to try next and when to call service.

* I would choose packaging before consumer assistants because we can look for a repeated machine design, someone responsible for the instructions, and a service team already spending money on the problem. I would target manufacturers that pay for substantial warranty or included support.

### What the operator sees

* Recovery shows one check from the manufacturer’s instructions and the events that explain why it applies. It remembers completed checks so the operator can move on to the next one.

* If records disagree or information is missing, it asks for clarification. If the checks keep failing, it sends the history to a service specialist.

* A person performs the check and confirms what happened. Recovery never resets the machine, changes settings or writes repair instructions.

### Why use Liquid

* I would start with LFM2.5 with 2.6B parameters to read operator notes. People describe the same problem in different ways. The model turns those notes into facts; ordinary software chooses the next approved check. If forms and simple rules do the job with less upkeep, we should use them.

* Running on the machine’s existing computer could keep the assistant available without internet access. We would first check available memory and performance, then compare the cost with a shared factory server or cloud service.

### The first eight weeks

* Use the first two weeks to review support cases and agree on instructions. Connect the data in weeks three and four. Let service staff review recommendations in weeks five and six, then try supervised use on two machines. Two engineers build it; I lead customer research and measure the results.

* The target is 25% less specialist time per relevant support case. We need to show that saving before expanding to more machines.

The demo uses invented incidents. The assistant and rules alone both passed 24 examples, so the test does not establish a need for the model. Customer savings and factory hardware performance still need testing. [Demo and results](https://liquid-recovery.vercel.app/) · [Liquid model card](https://huggingface.co/LiquidAI/LFM2.5-2.6B).

<!-- page break -->

RECOVERY  /  CUSTOMERS AND LONG TERM VALUE

## Customers and long term value

The service leader at an equipment manufacturer would buy Recovery from the service budget. This would be their first purchase from Liquid. They could include it in the support contracts they already sell to factories.

### Finding customers and testing the price

* Start with Douglas and Massman through industry introductions and PMMI, the packaging industry association. Ask each for 20 recent support cases and access to two customer plants. Recruit ten people across service, engineering, maintenance and operating shifts. These are prospects; I have not validated demand.

* Test a $20K eight week pilot, credited against the first year. Then charge $30K per manufacturer each year plus $300 per machine. At 200 machines, that is $90K a year.

* I would look for at least $180K in yearly value after setup and upkeep, from saved support time, avoided travel or added service profit. Four calls per machine, 20 minutes saved and $100 per hour produce only $26.7K. That customer would not justify the price.

### How the value grows over time

* Each machine builds a history of its software version, product settings, alarms, attempted checks and confirmed outcomes. Service engineers review recurring problems and improve the instructions and the examples used to interpret notes. The next operator starts with that knowledge.

* Those past cases also become tests that every update must pass. Over time, replacing Recovery would mean rebuilding and checking that machine knowledge. Customers would own and be able to export their records. We would keep their service knowledge separate.

* If models become interchangeable, customers would still pay for accurate machine connections, current instructions and updates they can trust. SOMIC, Pearson, Beckhoff and ei³ already offer relevant support tools. We have to show that ours takes less work to set up and maintain.

### Growing beyond the first customer

* Reuse the app, testing tools and update process. Change the machine connections and instructions for each manufacturer. A second machine should only need its data and instructions added. A second manufacturer must fit ten engineering days after access is ready, counting their preparation too. Expand to other equipment only after that works.

* Ten manufacturers with 200 machines each would bring in $900K a year. Fifty with 500 machines would bring in $9M. These are scenarios based on the proposed price. I still need to establish how many buyers fit.

* I would stop if we cannot get usable records or someone responsible for the instructions by week two, recommendations remain unreliable, support time does not fall, setup exceeds the time limit, hardware removes the savings, or buyers reject the price after seeing results.

Public sources: [Douglas](https://www.douglas-machine.com/products-solutions/case-and-tray-packers/), [Massman](https://massmanautomation.com/applications/cans-bottles/), [SOMIC](https://us.somic-packaging.com/service/digital-services/), [Pearson](https://pearsonpkg.com/technical-service/remote-service-support/), [Beckhoff](https://www.beckhoff.com/en-au/products/automation/twincat-projects-with-ai-supported-engineering/), [ei³](https://ei3.com/platform/iiot-feature/connected-ai). Capabilities vary by product. Codex helped with research, code, testing and writing under my direction.
