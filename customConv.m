% Code to perform convolution for signals and systems, ECS 204. SEM 4 summer 2025.
% using the inbuilt function to get familier wiht the environmnet nd
% running everything.
function y = performConvolution(x, h)
    y = conv(x, h);  % Perform convolution using MATLAB's conv function
end

function visualizeConvolution(x, h)
    % Plot the original signals
    figure;
    subplot(3, 1, 1);
    stem(x, 'b', 'LineWidth', 1.5);
    title('Signal x');
    xlabel('n');
    ylabel('x[n]');
    grid on;

    subplot(3, 1, 2);
    stem(h, 'r', 'LineWidth', 1.5);
    title('Signal h');
    xlabel('n');
    ylabel('h[n]');
    grid on;

    % Initialize the convolution result
    y = conv(x, h);
    
    % Plot convolution step by step
    subplot(3, 1, 3);
    hold on;
    title('Convolution Result');
    xlabel('n');
    ylabel('y[n]');
    grid on;
    
    % Perform convolution and update plot
    for k = 1:length(x)  % Limit to the length of x
        % Compute partial convolution result for current index k
        temp_y = conv(x(1:k), h);
        
        % Create a vector of indices for x-axis based on temp_y length
        temp_x = 0:length(temp_y)-1; 
        
        % Plot the partial convolution result
        plot(temp_x, temp_y, 'k', 'LineWidth', 1.5);
        pause(0.5);  % Pause to allow for visualization
    end
    hold off;
    disp('Convolution Complete!');
end


t = 0:0.1:2*pi; 
% Example signals
x = sin(t);
h = cos(t);
disp(performConvolution(x, h));  % Display the convolution result

visualizeConvolution(x, h);



% x = [1 2 3];  % First signal
% h = [4 5 6];  % Second signal

